import requests
import os
from dotenv import load_dotenv

load_dotenv()

def send_password_to_slack(password):
    webhook = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook:
        return False, "No webhook configured"

    # Fix: never log password in plaintext
    masked = password[:3] + "*" * (len(password) - 3)
    print(f"Sending password to Slack: {masked}")

    payload = {
        # Fix: removed response_type ephemeral — doesn't work with webhooks
        "text": f"🔐 Your generated password: `{password}`"
    }

    try:
        res = requests.post(webhook, json=payload, timeout=5)  # Fix: add timeout
        if res.status_code == 200:
            return True, "✅ Password sent to Slack!"
        return False, f"❌ Failed to send: {res.text}"
    except Exception as e:
        return False, f"❌ Slack error: {str(e)}"