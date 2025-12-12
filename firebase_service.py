import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime

# Globals
db = None
firebase_ok = False


# --- Initialize Firebase safely ---
try:
    # Try to load your Firebase credentials
    cred = credentials.Certificate("firebase_key.json")

    # Initialize the Firebase app (only once)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # Get Firestore client
    db = firestore.client()
    firebase_ok = True
    print("✅ Firebase initialized successfully.")

except Exception as e:
    print("⚠️ Firebase init failed:", e)
    print("Running in offline/demo mode.")
    firebase_ok = False


# --- USER MANAGEMENT ---

def create_user(email: str, password: str, name: str) -> str:
    """
    Creates a new Firebase user and saves basic info in Firestore.
    If Firebase isn't connected, returns a dummy ID.
    """
    if not firebase_ok:
        print("create_user() called, but Firebase not configured.")
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


def get_user_by_email(email: str):
    """
    Fetch a user's UID using their email.
    Returns None if not found.
    """
    if not firebase_ok:
        print("get_user_by_email() called, but Firebase not configured.")
        return "dummy-user-id"

    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except Exception:
        return None


# --- TRANSACTIONS MANAGEMENT ---

def add_transaction(user_id: str, customer_name: str, item: str, amount: float, t_type: str):
    """
    Add a transaction to the Firestore database.
    t_type can be 'sale', 'udhaar', or 'repayment'.
    """
    if not firebase_ok:
        print("add_transaction() called, but Firebase not configured.")
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

    print(f"Transaction added for {customer_name}: {item} - ₹{amount}")


def get_transactions(user_id: str):
    """
    Retrieve all transactions for a specific user, sorted by most recent.
    Returns an empty list if offline.
    """
    if not firebase_ok:
        print("get_transactions() called, but Firebase not configured.")
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
