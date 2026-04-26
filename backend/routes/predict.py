from flask import Blueprint, request, jsonify
import tensorflow as tf
import json
import os
import numpy as np
import sqlite3
from PIL import Image

# YOUR UTILS
try:
    from utils.predict import predict_disease
    from utils.recommendations import get_treatment_recommendation
    from utils.severity import calculate_severity
    print("✅ YOUR UTILS loaded!")
except ImportError:
    print("❌ Utils missing - create backend/utils/*.py")
    raise

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")

# PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "wheatshield_mobilenet.keras")
CLASS_IDX_PATH = os.path.join(BASE_DIR, "model", "class_indices.json")
DB_PATH = os.path.join(BASE_DIR, "database", "wheatshield.db")
UPLOAD_PATH = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_PATH, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# -------------------------
# MODEL ARCHITECTURE
# -------------------------
def build_wheatshield_model():
    """Exactly match the architecture you trained with"""
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3), 
        include_top=False, 
        weights=None 
    )
    
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(5, activation='softmax')
    ])
    return model

print("🔄 Building architecture and loading YOUR weights...")
try:
    model = build_wheatshield_model()
    model.load_weights(MODEL_PATH)
    print("✅ YOUR WEIGHTS LOADED SUCCESSFULLY!")
except Exception as e:
    print(f"❌ Failed to load weights: {e}")
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    print("✅ Fallback model loaded!")

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# CLASSES
with open(CLASS_IDX_PATH, "r") as f:
    class_indices = json.load(f)
idx_to_class = {v: k for k, v in class_indices.items()}
print(f"✅ YOUR {len(idx_to_class)} wheat disease classes loaded")

# -------------------------
# PREDICT ROUTE
# -------------------------
@predict_bp.route("", methods=["POST"])
def predict():
    file = request.files.get("image")
    
    # Try multiple ways to get the user_id from the frontend
    user_id = request.form.get("user_id") or request.args.get("user_id") or "unknown_user"
    
    print(f"DEBUG: Processing request for User ID: {user_id}")

    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    img_path = os.path.join(UPLOAD_PATH, "temp.jpg")
    file.save(img_path)

    try:
        # AI PREDICTION LOGIC
        img = Image.open(img_path).convert('RGB').resize((224, 224))
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_tensor = np.expand_dims(img_array, axis=0)
        
        disease, confidence = predict_disease(model, img_tensor, idx_to_class)
        fake_heatmap = np.full((224, 224), confidence)
        severity = calculate_severity(fake_heatmap, disease)
        recommendation = get_treatment_recommendation(disease)

        # DATABASE LOGIC (Corrected and Explicit)
        print(f"DEBUG: Constructing DB query for {user_id}")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Ensure table structure is always correct with timestamp
        c.execute("""CREATE TABLE IF NOT EXISTS history 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      user_id TEXT, 
                      disease TEXT, 
                      confidence REAL, 
                      severity TEXT, 
                      recommendation TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        
        # Explicit column mapping for safety
        c.execute("""INSERT INTO history (user_id, disease, confidence, severity, recommendation) 
                     VALUES (?, ?, ?, ?, ?)""",
                  (user_id, disease, float(confidence), severity, recommendation))
        
        conn.commit()
        conn.close()
        
        print(f"✅ LOG: Successfully saved record for {user_id}")

        return jsonify({
            "disease": disease,
            "confidence": round(float(confidence), 3),
            "severity": severity,
            "recommendation": recommendation
        })

    except Exception as e:
        print(f"❌ LOG ERROR: {str(e)}")
        return jsonify({"error": f"Prediction or saving failed: {str(e)}"}), 500
    
    finally:
        if os.path.exists(img_path):
            os.remove(img_path)

@predict_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "classes": len(idx_to_class),
        "db_path": DB_PATH
    })

print("🚀 WheatShield API ready!")