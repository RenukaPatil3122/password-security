# 🔐 Password Security System

A comprehensive password security toolkit that checks password strength, detects breached passwords using the **Have I Been Pwned (HIBP)** API, generates strong passwords, and sends **Slack notifications** for security alerts.

---

## ✨ Features

- 🔍 **Password Strength Checker** — Analyzes passwords for length, complexity, and common patterns
- 🌐 **Breach Detection** — Checks passwords against the HIBP database using k-anonymity (your password is never sent in plain text)
- 🔑 **Password Generator** — Generates cryptographically strong, customizable passwords
- 📣 **Slack Notifications** — Sends real-time alerts when weak or breached passwords are detected
- 🐳 **Dockerized** — Ready to run in any environment with Docker

---

## 🗂️ Project Structure

```
password-security/
├── app.py                  # Main application entry point
├── password_checker.py     # Password strength analysis logic
├── password_generator.py   # Secure password generation
├── hibp.py                 # Have I Been Pwned API integration
├── slack_notify.py         # Slack webhook notification handler
├── test_password.py        # Unit tests
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
└── .env                    # Environment variables (not committed)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- A [Slack Incoming Webhook URL](https://api.slack.com/messaging/webhooks) (optional)

### 1. Clone the repository
```bash
git clone https://github.com/RenukaPatil3122/password-security.git
cd password-security
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```env
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
```

### 5. Run the app
```bash
python app.py
```

---

## 🐳 Run with Docker

```bash
docker build -t password-security .
docker run --env-file .env password-security
```

---

## 🧪 Run Tests

```bash
pytest test_password.py
```

---

## 🔒 How HIBP Integration Works

This project uses the **k-anonymity model** to check passwords safely:
1. The password is hashed using SHA-1
2. Only the **first 5 characters** of the hash are sent to the HIBP API
3. The API returns all hashes starting with those 5 characters
4. The check happens **locally** — your full password never leaves your machine

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)

---

## ⚠️ Security Note

Never commit your `.env` file. Add it to `.gitignore`:
```
.env
venv/
__pycache__/
```

---

## 👩‍💻 Author

**Renuka Patil**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/renuka-patil123/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/RenukaPatil3122)
