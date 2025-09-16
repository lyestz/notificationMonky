import requests

BOT_TOKEN = "8296753617:AAEuM1TCmOGA3_YujdHzRBINEJOQXQEQ2Ss"
CHAT_ID = "-1002818920734"

def handler(request, response):
    try:
        body = request.json()
        message = body.get("message", "").strip()
        parse_mode = body.get("parse_mode", "HTML")

        if not message:
            return response.status(400).json({
                "status": "no",
                "error": "Message is empty"
            })

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": parse_mode
        }

        r = requests.post(url, json=payload, timeout=10)

        if r.ok:
            return response.status(200).json({
                "status": "ok",
                "message": "Message sent ✅"
            })
        else:
            return response.status(r.status_code).json({
                "status": "no",
                "error": r.text
            })

    except Exception as e:
        return response.status(500).json({
            "status": "no",
            "error": str(e)
        })
