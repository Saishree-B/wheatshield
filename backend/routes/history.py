from flask import Blueprint, request, jsonify
import sqlite3
import os

history_bp = Blueprint("history", __name__, url_prefix="/history")

# DYNAMIC PATH (FIX #1)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "wheatshield.db")

@history_bp.route("", methods=["GET"])
def get_history():
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify([])  # Empty list OK
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Add created_at if missing
        c.execute("PRAGMA table_info(history)")
        columns = [col[1] for col in c.fetchall()]
        if 'created_at' not in columns:
            c.execute("ALTER TABLE history ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
        
        c.execute("""
            SELECT disease, confidence, severity, recommendation, created_at
            FROM history WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
        
        rows = c.fetchall()
        conn.close()
        
        data = [{
            "disease": r[0],
            "confidence": float(r[1]),
            "severity": r[2],
            "recommendation": r[3],
            "created_at": r[4] if len(r) > 4 else "Just now"
        } for r in rows]
        
        return jsonify(data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route("/clear", methods=["POST"])
def clear_history():
    user_id = request.json.get("user_id") if request.is_json else request.form.get("user_id")
    
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
