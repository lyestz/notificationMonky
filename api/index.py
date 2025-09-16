from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import traceback

app = Flask(__name__)
CORS(app)

# Fixe directement les valeurs ici
BOT_TOKEN = "8296753617:AAEuM1TCmOGA3_YujdHzRBINEJOQXQEQ2Ss"
CHAT_ID = "-1002818920734"


@app.route("/api/send_message", methods=["POST"])
def send_message():
    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({
            "status": "no",
            "error": "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"
        }), 500

    try:
        body = request.get_json(force=True) or {}
        message = body.get("message", "").strip()
        parse_mode = body.get("parse_mode", "HTML")  # par défaut HTML

        if not message:
            return jsonify({"status": "no", "error": "Message is empty"}), 400

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": parse_mode
        }

        resp = requests.post(url, json=payload, timeout=10)

        if resp.ok:
            return jsonify({"status": "ok", "message": "Message sent ✅"}), 200
        else:
            return jsonify({
                "status": "no",
                "error": resp.text
            }), resp.status_code

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "status": "no",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
