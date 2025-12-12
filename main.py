# main.py

import streamlit as st
import matplotlib.pyplot as plt

from firebase_service import (
    create_user,
    get_user_by_email,
    add_transaction,
    get_transactions,
)
from ocr_service import extract_text_from_image, parse_bill_text
from voice_service import parse_command
from analytics import transactions_to_dataframe, compute_customer_udhaar


def init_session_state():
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None


def show_register():
    st.subheader("Register")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create account"):
        if not email or not password or not name:
            st.error("Please fill all fields.")
            return

        try:
            uid = create_user(email, password, name)
            st.success(f"Account created for {name}. You can now log in.")
            st.info(f"Your user ID (for debugging): {uid}")
        except Exception as e:
            st.error(f"Error creating user: {e}")


def show_login():
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # NOTE: In this simple demo, we're not verifying password against Firebase.
    # We only find user by email and "log in".
    if st.button("Login"):
        uid = get_user_by_email(email)
        if uid:
            st.session_state["user_id"] = uid
            st.session_state["user_email"] = email
            st.success("Logged in successfully.")
        else:
            st.error("User not found. Please register first.")


def show_upload_bill():
    st.subheader("Upload Bill (OCR)")

    if not st.session_state["user_id"]:
        st.warning("Please login first.")
        return

    uploaded_file = st.file_uploader("Upload bill image", type=["jpg", "jpeg", "png"])
    customer_name = st.text_input("Customer name", "Walk-in")

    if uploaded_file is not None and st.button("Process Bill"):
        with st.spinner("Running OCR..."):
            text = extract_text_from_image(uploaded_file)

        st.text_area("Extracted Text", text, height=150)

        items = parse_bill_text(text)
        if not items:
            st.warning("No items detected. Try a clearer image or different format.")
            return

        st.write("Detected items:")
        st.write(items)

        for item in items:
            add_transaction(
                st.session_state["user_id"],
                customer_name,
                item["item"],
                item["amount"],
                "sale",
            )
        st.success("Bill processed and transactions saved.")


def show_voice_command():
    st.subheader("Command (typed or from voice)")

    if not st.session_state["user_id"]:
        st.warning("Please login first.")
        return

    st.markdown(
        """
        **Command examples:**
        - `add udhaar Ramesh sugar 50`
        - `repayment Ramesh 100`
        """
    )

    # To avoid browser microphone complexity, we let user type the command
    command_text = st.text_input("Type or paste your command")

    if st.button("Run Command"):
        cmd = parse_command(command_text)
        st.write("Parsed command:", cmd)

        if cmd["action"] == "add_udhaar":
            add_transaction(
                st.session_state["user_id"],
                cmd["customer_name"],
                cmd["item"],
                cmd["amount"],
                "udhaar",
            )
            st.success("Udhaar transaction added.")
        elif cmd["action"] == "repayment":
            add_transaction(
                st.session_state["user_id"],
                cmd["customer_name"],
                "repayment",
                -cmd["amount"],
                "repayment",
            )
            st.success("Repayment recorded.")
        else:
            st.error("Could not understand command.")


def show_dashboard():
    st.subheader("Dashboard")

    if not st.session_state["user_id"]:
        st.warning("Please login first.")
        return

    transactions = get_transactions(st.session_state["user_id"])
    df = transactions_to_dataframe(transactions)

    if df.empty:
        st.info("No transactions yet. Upload a bill or add an udhaar.")
        return

    st.markdown("### All Transactions")
    st.dataframe(df)

    udhaar_df = compute_customer_udhaar(df)
    if udhaar_df is not None and not udhaar_df.empty:
        st.markdown("### Customer Udhaar Summary")
        st.dataframe(udhaar_df)

        # Plot top 5 customers by udhaar
        top5 = udhaar_df.head(5)

        fig, ax = plt.subplots()
        ax.bar(top5["customer_name"], top5["net_udhaar"])
        ax.set_xlabel("Customer")
        ax.set_ylabel("Net Udhaar")
        ax.set_title("Top Customers by Udhaar")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("No udhaar/repayment data yet.")


def main():
    st.set_page_config(page_title="SahaYOGI", layout="wide")
    init_session_state()

    st.title("SahaYOGI – AI Co-pilot for Small Shops")

    menu = ["Login", "Register", "Upload Bill", "Command", "Dashboard"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        show_login()
    elif choice == "Register":
        show_register()
    elif choice == "Upload Bill":
        show_upload_bill()
    elif choice == "Command":
        show_voice_command()
    elif choice == "Dashboard":
        show_dashboard()


if __name__ == "__main__":
    main()
