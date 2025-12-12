# firebase_service.py

import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime

# Initialize Firebase app
cred = credentials.Certificate("firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()


def create_user(email: str, password: str, name: str) -> str:
    """
    Create a new user in Firebase Auth and Firestore.
    Returns the user_id (UID).
    """
    try:
        user = auth.create_user(email=email, password=password)
    except Exception as e:
        # If user already exists, get the existing one
        try:
            user = auth.get_user_by_email(email)
        except Exception as e2:
            raise e2

    user_doc = {
        "name": name,
        "email": email,
    }
    db.collection("users").document(user.uid).set(user_doc)
    return user.uid


def get_user_by_email(email: str):
    """
    Fetch user by email. Returns user_id (UID) or None.
    """
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception:
        return None


def add_customer(user_id: str, customer_name: str):
    """
    Add or update a customer document under the shop.
    """
    ref = db.collection("shops").document(user_id)\
           .collection("customers").document(customer_name)
    ref.set({"name": customer_name})


def get_customers(user_id: str):
    """
    Return list of customer dicts for a given shop.
    """
    docs = db.collection("shops").document(user_id)\
        .collection("customers").stream()
    return [doc.to_dict() for doc in docs]


def add_transaction(user_id: str, customer_name: str,
                    item: str, amount: float, t_type: str):
    """
    Add a transaction under the shop's transactions subcollection.
    """
    data = {
        "customer_name": customer_name,
        "item": item,
        "amount": float(amount),
        "type": t_type,
        "timestamp": datetime.utcnow()
    }

    db.collection("shops").document(user_id)\
      .collection("transactions").add(data)

    # Optionally ensure customer exists
    add_customer(user_id, customer_name)


def get_transactions(user_id: str):
    """
    Return list of transaction dicts for a given shop, sorted by time.
    """
    docs = db.collection("shops").document(user_id)\
        .collection("transactions")\
        .order_by("timestamp", direction=firestore.Query.DESCENDING)\
        .stream()

    return [doc.to_dict() for doc in docs]
