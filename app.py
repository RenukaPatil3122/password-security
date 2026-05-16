from flask import Flask, request, jsonify
from password_checker import check_password
from password_generator import generate_password
from hibp import check_hibp
from slack_notify import send_password_to_slack
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    password = data.get("password", "")

    if not password:
        return jsonify({"error": "No password provided"}), 400

    # Fix: prevent abuse — cap input length
    if len(password) > 128:
        return jsonify({"error": "Password too long"}), 400

    strong, messages = check_password(password)
    breached, hibp_msg = check_hibp(password)

    return jsonify({
        "strong": strong and not breached,
        "strength_messages": messages,
        "hibp_message": hibp_msg,
        "breached": breached
    })

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    length = data.get("length", 16)
    no_symbols = data.get("no_symbols", False)

    # Fix: validate inputs
    if not isinstance(length, int) or length < 16 or length > 24:
        return jsonify({"error": "Length must be an integer between 16 and 24"}), 400

    if not isinstance(no_symbols, bool):
        return jsonify({"error": "no_symbols must be true or false"}), 400

    password = generate_password(length=length, no_symbols=no_symbols)
    success, msg = send_password_to_slack(password)

    return jsonify({
        # Fix: never return raw password in API response
        "password_hint": password[:3] + "*" * (len(password) - 3),
        "slack_status": msg
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)