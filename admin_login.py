"""
Lucky Draw - Admin Login Script
Logs in as admin via the UI /login form endpoint.

Usage:
    python3 admin_login.py

Env overrides:
    UI_URL      default: http://localhost:80
    USERNAME    default: admin
    PASSWORD    default: admin123
"""

import os
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

UI_URL   = os.getenv("UI_URL", "http://localhost:80")
USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "admin123")

LOGIN_URL = UI_URL + "/login"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


_opener = urllib.request.build_opener(NoRedirect)


def login():

    payload = urllib.parse.urlencode({
        "username": USERNAME,
        "password": PASSWORD
    }).encode()

    req = urllib.request.Request(
        LOGIN_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )

    ts = datetime.now().strftime("%H:%M:%S")

    try:

        with _opener.open(req, timeout=10) as resp:
            print(f"[{ts}] ✓ {resp.status} | Login successful as '{USERNAME}'", flush=True)

    except urllib.error.HTTPError as e:
        print(f"[{ts}] ✗ HTTP {e.code} | {e.reason}", flush=True)

    except Exception as e:
        print(f"[{ts}] ✗ ERROR | {e}", flush=True)


if __name__ == "__main__":
    print(f"Admin login → {LOGIN_URL} (every 5s)", flush=True)

    while True:
        login()
        time.sleep(5)
