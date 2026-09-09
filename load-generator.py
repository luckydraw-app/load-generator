"""
Lucky Draw - Participation Load Generator
Sends random participate requests via the UI /participate form endpoint.

Usage:
    python3 load_generator.py

Env overrides:
    UI_URL              default: http://localhost:8080
    MIN_DELAY_SECONDS   default: 30
    MAX_DELAY_SECONDS   default: 60
"""

import os
import time
import random
import string
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────

PARTICIPATE_URL = os.getenv("UI_URL", "http://localhost:8080") + "/participate"

MIN_DELAY = int(os.getenv("MIN_DELAY_SECONDS", 1))
MAX_DELAY = int(os.getenv("MAX_DELAY_SECONDS", 10))

# ──────────────────────────────────────────────
# Data pools
# ──────────────────────────────────────────────

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun",
    "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Priya", "Ananya", "Isha", "Diya", "Kavya",
    "Pooja", "Sneha", "Riya", "Meera", "Nisha",
    "Rahul", "Rohit", "Amit", "Suresh", "Vijay",
    "Neha", "Anjali", "Sunita", "Rekha", "Geeta",
    "James", "Oliver", "Harry", "Jack", "George",
    "Emily", "Olivia", "Isla", "Amelia", "Ava",
    "Liam", "Noah", "Ethan", "Lucas", "Mason",
    "Sophia", "Emma", "Charlotte", "Mia", "Harper"
]

LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Singh", "Kumar",
    "Gupta", "Joshi", "Mehta", "Shah", "Yadav",
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Wilson", "Moore",
    "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Robinson", "Clark"
]

DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com",
    "hotmail.com", "example.com", "mail.com",
    "proton.me", "icloud.com"
]


# ──────────────────────────────────────────────
# Generator
# ──────────────────────────────────────────────

def random_suffix(length=4):
    return ''.join(random.choices(string.digits, k=length))


def random_user():

    first = random.choice(FIRST_NAMES)
    last  = random.choice(LAST_NAMES)
    suffix = random_suffix()

    name  = f"{first} {last}"
    email = f"{first.lower()}.{last.lower()}{suffix}@{random.choice(DOMAINS)}"
    phone = f"9{''.join(random.choices(string.digits, k=9))}"

    return {
        "name":  name,
        "email": email,
        "phone": phone
    }


# ──────────────────────────────────────────────
# Sender
# ──────────────────────────────────────────────

def send(user):

    payload = urllib.parse.urlencode(user).encode()

    req = urllib.request.Request(
        PARTICIPATE_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )

    try:

        with urllib.request.urlopen(req, timeout=10) as resp:

            ts = datetime.now().strftime("%H:%M:%S")

            print(
                f"[{ts}] ✓ {resp.status} | "
                f"{user['name']:<25} | "
                f"{user['phone']} | "
                f"{user['email']}",
                flush=True
            )

    except urllib.error.HTTPError as e:

        ts = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{ts}] ✗ HTTP {e.code} | "
            f"{user['name']} | {e.reason}",
            flush=True
        )

    except Exception as e:

        ts = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{ts}] ✗ ERROR | {user['name']} | {e}",
            flush=True
        )


# ──────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────

if __name__ == "__main__":

    print(f"Load generator started → {PARTICIPATE_URL} (via UI)", flush=True)
    print(f"Delay range: {MIN_DELAY}s – {MAX_DELAY}s per request\n", flush=True)

    while True:

        user  = random_user()
        delay = random.randint(MIN_DELAY, MAX_DELAY)

        send(user)

        print(f"  → next request in {delay}s", flush=True)

        time.sleep(delay)
