import secrets
import string

def generate_password(length=16, no_symbols=False):
    if length < 16:
        length = 16
    if length > 24:
        length = 24

    if no_symbols:
        chars = string.ascii_letters + string.digits
    else:
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"

    while True:
        pwd = ''.join(secrets.choice(chars) for _ in range(length))
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_digit = any(c.isdigit() for c in pwd)
        has_symbol = any(c in "!@#$%^&*()" for c in pwd)

        if no_symbols:
            if has_upper and has_lower and has_digit:
                return pwd
        else:
            if has_upper and has_lower and has_digit and has_symbol:
                return pwd