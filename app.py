from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
from functools import wraps
from dotenv import load_dotenv
import os
import config

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BACKEND_API_KEY = os.getenv("API_KEY")  

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")
if not BACKEND_API_KEY:
    raise ValueError("API_KEY is not set in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)

CORS(app, resources={r"/*": {"origins": [
    "https://translation-web-app-frontend.vercel.app",
    "http://localhost:3000"
]}})

# Decorator to require API key authentication
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        client_key = request.headers.get("X-API-KEY")
        if not client_key or client_key != BACKEND_API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/auto-translate', methods=['POST'])
@require_api_key
def auto_translate():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    text = data.get("text")
    target = data.get("target")

    if not text or not target:
        return jsonify({"error": "Missing 'text' or 'target'"}), 400

    try:
        detected = config.detect_language(text)
        translated = config.gemini_translate(text, detected, target)
        return jsonify({"detected": detected, "translated": translated})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
