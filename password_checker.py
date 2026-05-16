import re

def check_password(password):
    errors = []

    if len(password) < 12:
        errors.append("❌ Too short (minimum 12 characters)")

    if not re.search(r'[A-Z]', password):
        errors.append("❌ Missing uppercase letter")

    if not re.search(r'[a-z]', password):
        errors.append("❌ Missing lowercase letter")

    if not re.search(r'[0-9]', password):
        errors.append("❌ Missing number")

    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        errors.append("❌ Missing special character")

    if errors:
        return False, errors
    return True, ["✅ Password is strong!"]