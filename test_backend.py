# test_backend.py

from firebase_service import create_user, add_transaction, get_transactions

if __name__ == "__main__":
    email = "testshop@example.com"
    password = "password123"
    name = "Test Shop"

    uid = create_user(email, password, name)
    print("User ID:", uid)

    add_transaction(uid, "Ramesh", "Sugar 1kg", 50, "udhaar")
    add_transaction(uid, "Ramesh", "repayment", -20, "repayment")

    txns = get_transactions(uid)
    print("Transactions:")
    for t in txns:
        print(t)
