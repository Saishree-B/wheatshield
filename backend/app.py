from flask import Flask
from flask_cors import CORS
from routes.predict import predict_bp
from routes.history import history_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(predict_bp)
app.register_blueprint(history_bp)

if __name__ == "__main__":
    print("🚀 Starting WheatShield API...")
    app.run(debug=True, host="0.0.0.0", port=5000)
