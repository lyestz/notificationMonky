import requests
import json

BOT_TOKEN = "8296753617:AAEuM1TCmOGA3_YujdHzRBINEJOQXQEQ2Ss"
CHAT_ID = "-1002818920734"

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}

def handler(request):
    # Gestion du preflight (OPTIONS)
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": ""
        }

    try:
        body = json.loads(request.body.decode("utf-8"))
        message = body.get("message", "").strip()
        parse_mode = body.get("parse_mode", "HTML")

        if not message:
            return {
                "statusCode": 400,
                "headers": {**CORS_HEADERS, "Content-Type": "application/json"},
                "body": json.dumps({"status": "no", "error": "Message is empty"})
            }

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": parse_mode
        }

        r = requests.post(url, json=payload, timeout=10)

        if r.ok:
            return {
                "statusCode": 200,
                "headers": {**CORS_HEADERS, "Content-Type": "application/json"},
                "body": json.dumps({"status": "ok", "message": "Message sent ✅"})
            }
        else:
            return {
                "statusCode": r.status_code,
                "headers": {**CORS_HEADERS, "Content-Type": "application/json"},
                "body": json.dumps({"status": "no", "error": r.text})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {**CORS_HEADERS, "Content-Type": "application/json"},
            "body": json.dumps({"status": "no", "error": str(e)})
        }
