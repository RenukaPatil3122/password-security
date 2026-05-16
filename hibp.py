import hashlib
import requests
import time

def check_hibp(password, retries=3):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    for attempt in range(retries):
        try:
            res = requests.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                headers={"Add-Padding": "true"},
                timeout=5  # Fix: always set timeout
            )
            hashes = res.text.splitlines()
            for line in hashes:
                h, count = line.split(":") ##h is hibp suffix 
                if h == suffix:
                    return True, f"❌ Found in breach database ({count} times!)"
            return False, "✅ Not found in any breach database"

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            # Fix: strict fail — block password if HIBP unreachable
            return True, "⚠️ Could not verify with HIBP. Please try again later."