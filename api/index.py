import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/send_message", methods=["POST"])
def send_message():
    # Telegram bot credentials from Vercel environment variables
    bot_token = "8296753617:AAEuM1TCmOGA3_YujdHzRBINEJOQXQEQ2Ss"
    chat_id = "-1002818920734"

    if not bot_token or not chat_id:
        return jsonify({"error": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"}), 500

    try:
        body = request.get_json(force=True)
        message = body.get("message", "No message provided")
        parse_mode = body.get("parse_mode", "HTML")  # default to HTML
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode
    }

    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            return jsonify({"success": True, "message": "Message sent"}), 200
        else:
            return jsonify({"error": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500