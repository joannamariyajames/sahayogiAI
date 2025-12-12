import firebase_admin
import random
import string
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from firebase_admin import credentials, firestore, auth
import requests  # for SendGrid HTTP API


# ---------------- EMAIL / SENDGRID CONFIG ---------------- #

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_SENDER_EMAIL = os.getenv("SENDGRID_SENDER_EMAIL")


def send_login_otp_email(email: str, code: str) -> Tuple[bool, str]:
    """
    Send the login OTP code to user's email using SendGrid.

    Returns:
        (success: bool, message: str)
    """
    if not SENDGRID_API_KEY or not SENDGRID_SENDER_EMAIL:
        msg = "SendGrid credentials not set. Cannot send email."
        print("⚠️", msg)
        return False, msg

    body = f"""
Namaste 👋

Your SahaYOGI login OTP is: {code}

This OTP is valid for 10 minutes.
If you didn’t request this, you can ignore this email.

– Team SahaYOGI
"""

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "personalizations": [
            {
                "to": [{"email": email}],
            }
        ],
        "from": {
            "email": SENDGRID_SENDER_EMAIL,
            "name": "SahaYOGI",
        },
        "subject": "SahaYOGI Login OTP",
        "content": [
            {
                "type": "text/plain",
                "value": body,
            }
        ],
    }

    try:
        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code in (200, 202):
            print(f"✅ OTP email sent to {email} via SendGrid")
            return True, "OTP email sent successfully."
        else:
            err = f"SendGrid error {resp.status_code}: {resp.text}"
            print("⚠️", err)
            return False, err
    except Exception as e:
        err = f"Exception while sending email via SendGrid: {e}"
        print("⚠️", err)
        return False, err


# ---------------- FIREBASE INIT ---------------- #

db = None
firebase_ok = False

try:
    cred = credentials.Certificate("firebase_key.json")

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    firebase_ok = True
    print("✅ Firebase initialized successfully.")

except Exception as e:
    print("⚠️ Firebase init failed:", e)
    firebase_ok = False


# ---------------- USER FUNCTIONS ---------------- #

def create_user(email: str, password: str, name: str) -> str:
    if not firebase_ok:
        print("create_user() called but Firebase not configured.")
        return "dummy-user-id"

    try:
        user = auth.create_user(email=email, password=password)
        print(f"User created: {user.uid}")
    except Exception:
        user = auth.get_user_by_email(email)
        print(f"User already exists: {user.uid}")

    user_doc = {"name": name, "email": email}
    db.collection("users").document(user.uid).set(user_doc)
    return user.uid


def get_user_by_email(email: str) -> Optional[str]:
    if not firebase_ok:
        print("get_user_by_email() called but Firebase not configured.")
        return None

    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception:
        return None


# ---------------- TRANSACTION FUNCTIONS ---------------- #

def add_transaction(
    user_id: str,
    customer_name: str,
    item: str,
    amount: float,
    t_type: str,
) -> None:
    if not firebase_ok:
        print("add_transaction() called but Firebase not configured.")
        return

    data = {
        "customer_name": customer_name,
        "item": item,
        "amount": float(amount),
        "type": t_type,
        "timestamp": datetime.utcnow(),
    }

    (
        db.collection("shops")
        .document(user_id)
        .collection("transactions")
        .add(data)
    )

    print(f"Transaction added for {customer_name}: {item} - ₹{amount} ({t_type})")


def get_transactions(user_id: str):
    if not firebase_ok:
        print("get_transactions() called but Firebase not configured.")
        return []

    try:
        docs = (
            db.collection("shops")
            .document(user_id)
            .collection("transactions")
            .order_by("timestamp", direction=firestore.Query.DESCENDING)
            .stream()
        )
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print("Error fetching transactions:", e)
        return []


# ---------------- OTP LOGIN HELPERS ---------------- #

def _generate_otp(length: int = 6) -> str:
    """Generate a numeric OTP code."""
    return "".join(random.choices(string.digits, k=length))


def ensure_user_exists(email: str) -> str:
    """
    Make sure a Firebase Auth user exists for this email.
    Returns the UID.
    """
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except auth.UserNotFoundError:
        user = auth.create_user(email=email)
        return user.uid


def create_login_otp(email: str, expires_in_minutes: int = 10) -> Optional[str]:
    """
    Create or overwrite an OTP for this email and store it in Firestore.

    Firestore doc path: login_otps/{email}
    Fields:
      - code
      - uid
      - created_at
      - expires_at
      - used
    """
    if not firebase_ok:
        print("create_login_otp() called but Firebase not configured.")
        return None

    uid = ensure_user_exists(email)
    code = _generate_otp()

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=expires_in_minutes)

    doc_ref = db.collection("login_otps").document(email)
    doc_ref.set(
        {
            "uid": uid,
            "code": code,
            "created_at": now,
            "expires_at": expires_at,
            "used": False,
        }
    )

    return code


def verify_login_otp(email: str, code: str) -> Optional[str]:
    """
    Verify an OTP for email.

    Returns:
      - UID (str) if valid
      - None if invalid / expired / not found
    """
    if not firebase_ok:
        print("verify_login_otp() called but Firebase not configured.")
        return None

    doc_ref = db.collection("login_otps").document(email)
    doc = doc_ref.get()

    if not doc.exists:
        return None

    data = doc.to_dict()
    if data.get("used"):
        return None

    if data.get("code") != code:
        return None

    # Check expiry
    expires_at = data.get("expires_at")
    if isinstance(expires_at, datetime):
        now = datetime.now(timezone.utc)
        if now > expires_at:
            return None

    # Mark OTP as used
    doc_ref.update({"used": True})

    return data.get("uid")
