from streamlit_cropper import st_cropper
from PIL import Image
import pytesseract
from chatbot_service import get_chat_response
import streamlit as st
import matplotlib.pyplot as plt
import time
import random
import pandas as pd  # NEW

from excel import (          # NEW
    append_to_excel,
    load_excel_data,
    calculate_summary,
    save_excel_data,
)

from streamlit_lottie import st_lottie
import json
import requests

from firebase_service import (
    create_user,
    get_user_by_email,
    add_transaction,
    get_transactions,
    create_login_otp,
    verify_login_otp,
    send_login_otp_email,
)
from ocr_service import extract_text_from_image, parse_bill_text
from voice_service import parse_command
from analytics import transactions_to_dataframe, compute_customer_udhaar


def init_session_state():
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None
    if "animation_loaded" not in st.session_state:
        st.session_state["animation_loaded"] = False
    # OTP-related state
    if "otp_sent" not in st.session_state:
        st.session_state["otp_sent"] = False
    if "pending_email" not in st.session_state:
        st.session_state["pending_email"] = ""
    # 💬 Chatbot history state (ADDED)
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


# ---------------- REGISTER ----------------
def show_register():
    with st.container():
        st.markdown(
            """
<style>
.register-container {
    background-color: rgba(255, 255, 255, 0.9);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(4px);
}
.register-container h2,
.register-container label,
.register-container p {
    color: #2c3e50 !important;
}
</style>
""",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="register-container">', unsafe_allow_html=True)

        st.markdown(
            '<h2 style="color:#2c3e50; margin-bottom: 0.5rem;">📝 Create New Account</h2>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            password = st.text_input(
                "Password", type="password", placeholder="Create a strong password"
            )

            if st.button("✨ Create Account", use_container_width=True):
                if not email or not password or not name:
                    st.error("Please fill all fields.")
                    return

                try:
                    uid = create_user(email, password, name)
                    st.success(f"🎉 Welcome {name}! Account created successfully.")

                    confetti_html = """
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
<script>
confetti({
    particleCount: 100,
    spread: 70,
    origin: { y: 0.6 }
});
</script>
"""
                    st.components.v1.html(confetti_html, height=100)

                    time.sleep(2)
                    st.info(f"🎯 Your Shop ID: *{uid[:8]}...*")
                except Exception as e:
                    st.error(f"❌ Error creating user: {e}")

        with col2:
            lottie_url = "https://assets10.lottiefiles.com/packages/lf20_qnq6r0tf.json"
            animation = load_lottie_url(lottie_url)
            if animation:
                st_lottie(animation, height=200, key="register_animation")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------- LOGIN (OTP-BASED) ----------------
def show_login():
    with st.container():
        st.markdown(
            """
<style>
.login-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 40px;
    border-radius: 25px;
    color: white;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.login-container label,
.login-container p {
    color: #f5f5ff !important;
}
</style>
""",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(
                '<h2 style="color:#ffffff; margin-bottom: 0.25rem;">🔐 OTP Login</h2>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='color:#f5f5ff;'>Login to your SahaYOGI dashboard with email OTP</p>",
                unsafe_allow_html=True,
            )

            # STEP 1: email input
            email = st.text_input(
                "Email",
                placeholder="shopkeeper@email.com",
                value=st.session_state.get("pending_email", ""),
            )

            col_send, col_status = st.columns([1, 2])
            with col_send:
                if st.button("📨 Send OTP", use_container_width=True):
                    if not email:
                        st.error("Please enter your email.")
                    else:
                        code = create_login_otp(email)
                        if code is None:
                            st.error("Firebase is not configured. Cannot create OTP.")
                        else:
                            success, msg = send_login_otp_email(email, code)
                            if success:
                                st.session_state["otp_sent"] = True
                                st.session_state["pending_email"] = email
                                st.success(f"✅ {msg} Check {email} (and Spam).")
                            else:
                              st.error(f"❌ Failed to send OTP: {msg}")

            with col_status:
                if st.session_state.get("otp_sent"):
                    st.info("✅ OTP has been sent. Enter it below to login.")

            # STEP 2: OTP input & verification
            otp_code = st.text_input(
                "Enter OTP",
                placeholder="6-digit code from your email",
                max_chars=6,
            )

            if st.button("🚀 Verify OTP & Login", use_container_width=True):
                if not st.session_state.get("pending_email"):
                    st.error("Please request an OTP first.")
                elif not otp_code:
                    st.error("Please enter the OTP.")
                else:
                    uid = verify_login_otp(st.session_state["pending_email"], otp_code)
                    if uid:
                        st.session_state["user_id"] = uid
                        st.session_state["user_email"] = st.session_state["pending_email"]
                        st.session_state["otp_sent"] = False
                        st.success("✅ Login successful! Redirecting...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid or expired OTP. Please try again.")

        with col2:
            lottie_url = "https://assets10.lottiefiles.com/packages/lf20_u8jppxsl.json"
            animation = load_lottie_url(lottie_url)
            if animation:
                st_lottie(animation, height=250, key="login_animation")

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------- UPLOAD BILL (WITH CROPPING) ----------------
def show_upload_bill():
    st.markdown(
        """
<style>
.upload-area {
    border: 3px dashed #4CAF50;
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    background: rgba(76, 175, 80, 0.1);
    transition: all 0.3s ease;
}
.upload-area:hover {
    background: rgba(76, 175, 80, 0.2);
    transform: scale(1.02);
}
</style>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h2 style="color:#2c3e50; margin-bottom:0.25rem;">🧾 Smart Bill Scanner</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='color:#333333; margin-bottom:1.5rem;'>Upload and crop the bill to extract items accurately!</p>",
        unsafe_allow_html=True,
    )

    if not st.session_state["user_id"]:
        st.warning("🔒 Please login first.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "📤 Upload bill image",
            type=["jpg", "jpeg", "png"],
            help="Upload clear images for best results",
        )
        st.markdown("</div>", unsafe_allow_html=True)

        customer_name = st.text_input(
            "👤 Customer Name",
            "Walk-in Customer",
            help="Enter customer name for record keeping",
        )

    with col2:
        lottie_url = "https://assets2.lottiefiles.com/packages/lf20_4chtx4vv.json"
        animation = load_lottie_url(lottie_url)
        if animation:
            st_lottie(animation, height=200, key="scanner_animation")

    if uploaded_file is not None:
        st.markdown("### ✂️ Crop the bill to the items section")

        img = Image.open(uploaded_file)

        cropped_img = st_cropper(
            img,
            realtime_update=True,
            box_color="#4CAF50",
            aspect_ratio=None,
        )

        st.markdown("### 📸 Cropped Preview")
        st.image(cropped_img, use_column_width=True)

        if st.button("🔍 Extract Items with AI", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            for percent_complete in range(0, 101, 20):
                status_text.text(f"Processing... {percent_complete}%")
                progress_bar.progress(percent_complete)
                time.sleep(0.1)

            with st.spinner("🤖 AI is reading your bill..."):
                text = pytesseract.image_to_string(cropped_img)

            progress_bar.progress(100)
            status_text.text("✅ Processing complete!")

            with st.expander("📝 View Extracted Text", expanded=True):
                st.text_area("", text, height=150, label_visibility="collapsed")

            items = parse_bill_text(text)

            if not items:
                st.warning("⚠️ No items found! Try cropping tighter or using a clearer image.")
                return

            st.markdown("### 🛍️ Detected Items")
            items_container = st.container()
            with items_container:
                for idx, item in enumerate(items):
                    st.markdown(
                        f"""
<div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
           padding: 15px;
           border-radius: 10px;
           margin: 10px 0;
           border-left: 5px solid #4CAF50;">
   <div style="display: flex; justify-content: space-between;">
       <span style="font-weight: bold; color:#2c3e50;">{item['item']}</span>
       <span style="color: #2E7D32; font-weight: bold;">₹{item['amount']}</span>
   </div>
</div>
""",
                        unsafe_allow_html=True,
                    )

            if st.button("💾 Save Transactions", use_container_width=True):
                for item in items:
                    add_transaction(
                        st.session_state["user_id"],
                        customer_name,
                        item["item"],
                        item["amount"],
                        "sale",
                    )
                    # also log into Excel "database"
                    append_to_excel(
                        st.session_state["user_id"],
                        customer_name,
                        item["item"],
                        item["amount"],
                        "sale",
                    )
                st.success(f"✅ Bill saved for {customer_name}!")
                time.sleep(2)
                st.balloons()


# ---------------- VOICE COMMAND ----------------
def show_voice_command():
    st.subheader("🎤 Voice & Text Commands")
    st.markdown(
        """
<style>
.command-box {
   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   padding: 20px;
   border-radius: 15px;
   color: white;
   margin: 20px 0;
}
</style>
""",
        unsafe_allow_html=True,
    )

    if not st.session_state["user_id"]:
        st.warning("🔒 Please login first.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            """
<div class="command-box">
   <h4>💡 Try these commands:</h4>
   <ul>
       <li><code>add udhaar Ramesh sugar 50</code></li>
       <li><code>repayment Ramesh 100</code></li>
       <li><code>add sale CustomerName item price</code></li>
   </ul>
</div>
""",
            unsafe_allow_html=True,
        )

        command_text = st.text_area(
            "📝 Type your command here:",
            height=100,
            placeholder="Speak or type your command...",
            help="Use natural language commands",
        )

    with col2:
        lottie_url = "https://assets10.lottiefiles.com/packages/lf20_gn0to0ab.json"
        animation = load_lottie_url(lottie_url)
        if animation:
            st_lottie(animation, height=200, key="voice_animation")

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        if st.button(
            "🎙️ Record Voice",
            use_container_width=True,
            disabled=True,
            help="Voice recording feature coming soon!",
        ):
            st.info("Voice recording feature is coming soon!")

    with col_btn2:
        if st.button("🚀 Execute Command", use_container_width=True, type="primary"):
            if command_text.strip():
                cmd = parse_command(command_text)

                with st.spinner("🤖 Processing your command..."):
                    time.sleep(1)

                st.markdown(
                    f"""
<div style="background: #E3F2FD; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3;">
<strong>📊 Parsed Command:</strong><br>
• Action: {cmd.get('action', 'N/A')}<br>
• Customer: {cmd.get('customer_name', 'N/A')}<br>
• Item: {cmd.get('item', 'N/A')}<br>
• Amount: {cmd.get('amount', 'N/A')}
</div>
""",
                    unsafe_allow_html=True,
                )

                if cmd["action"] == "add_udhaar":
                    add_transaction(
                        st.session_state["user_id"],
                        cmd["customer_name"],
                        cmd["item"],
                        cmd["amount"],
                        "udhaar",
                    )
                    append_to_excel(
                        st.session_state["user_id"],
                        cmd["customer_name"],
                        cmd["item"],
                        cmd["amount"],
                        "udhaar",
                    )
                    st.success(f"✅ Udhaar added for {cmd['customer_name']}!")
                elif cmd["action"] == "repayment":
                    add_transaction(
                        st.session_state["user_id"],
                        cmd["customer_name"],
                        "repayment",
                        -cmd["amount"],
                        "repayment",
                    )
                    append_to_excel(
                        st.session_state["user_id"],
                        cmd["customer_name"],
                        "repayment",
                        -cmd["amount"],
                        "repayment",
                    )
                    st.success(f"✅ Repayment recorded for {cmd['customer_name']}!")
                else:
                    st.error("❌ Could not understand command. Try again!")
            else:
                st.warning("⚠️ Please enter a command!")


# ---------------- 💬 CHATBOT (ADDED) ----------------
def show_chatbot():
    st.subheader("💬 SahaYOGI Chatbot")

    if not st.session_state["user_id"]:
        st.warning("🔒 Please login first.")
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        user_message = st.text_area(
            "Ask SahaYOGI anything about your shop:",
            placeholder="Example: What is my total udhaar? How do I manage profit and loss?",
            height=100,
            key="chat_input",
        )
    with col2:
        lottie_url = "https://assets10.lottiefiles.com/packages/lf20_xh7zbbbj.json"
        animation = load_lottie_url(lottie_url)
        if animation:
            st_lottie(animation, height=150, key="chatbot_animation")

    if st.button("🚀 Ask AI", use_container_width=True):
        if not user_message.strip():
            st.warning("Please type a question first.")
        else:
            # Optional: pass some context about this shop
            transactions = get_transactions(st.session_state["user_id"])
            df = transactions_to_dataframe(transactions)
            shop_context = ""
            if not df.empty:
                total_sales = df[df["type"] == "sale"]["amount"].sum()
                total_udhaar = df[df["type"] == "udhaar"]["amount"].sum()
                customers = df["customer_name"].nunique()
                shop_context = (
                    f"This shop has total sales of ₹{total_sales}, "
                    f"total udhaar of ₹{total_udhaar}, and {customers} customers in the database."
                )

            with st.spinner("🤖 SahaYOGI is thinking..."):
                reply = get_chat_response(user_message, shop_context=shop_context)

            # Save conversation to session
            st.session_state["chat_history"].append(("You", user_message))
            st.session_state["chat_history"].append(("SahaYOGI", reply))

    # Show chat history
    if st.session_state["chat_history"]:
        st.markdown("### 🗨️ Conversation")
        for sender, msg in st.session_state["chat_history"]:
            if sender == "You":
                st.markdown(
                    f"""
<div style="background:#E3F2FD;
            padding:10px;
            border-radius:10px;
            margin-bottom:5px;">
<b>👤 {sender}:</b> {msg}
</div>
""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
<div style="background:#F1F8E9;
            padding:10px;
            border-radius:10px;
            margin-bottom:5px;">
<b>🤖 {sender}:</b> {msg}
</div>
""",
                    unsafe_allow_html=True,
                )


# ---------------- DASHBOARD ----------------
def show_dashboard():
    st.subheader("📊 Smart Dashboard")

    if not st.session_state["user_id"]:
        st.warning("🔒 Please login first.")
        return

    # ---------- FIREBASE TRANSACTIONS ----------
    transactions = get_transactions(st.session_state["user_id"])
    df = transactions_to_dataframe(transactions)

    if df.empty:
        col1, col2 = st.columns([1, 2])
        with col1:
            lottie_url = "https://assets4.lottiefiles.com/packages/lf20_uq7gq2gf.json"
            animation = load_lottie_url(lottie_url)
            if animation:
                st_lottie(animation, height=300, key="empty_dashboard")

        with col2:
            st.info(
                "🌟 No transactions yet. Start by uploading a bill or adding an udhaar!"
            )
        return

    # ---------- TOP CARDS ----------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
           padding: 20px;
           border-radius: 15px;
           color: white;
           text-align: center;">
   <h3>💰</h3>
   <h2>{}</h2>
   <p>Total Sales</p>
</div>
""".format(
                len(df[df["type"] == "sale"])
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
           padding: 20px;
           border-radius: 15px;
           color: white;
           text-align: center;">
   <h3>📋</h3>
   <h2>{}</h2>
   <p>Total Udhaars</p>
</div>
""".format(
                len(df[df["type"] == "udhaar"])
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
           padding: 20px;
           border-radius: 15px;
           color: white;
           text-align: center;">
   <h3>👥</h3>
   <h2>{}</h2>
   <p>Customers</p>
</div>
""".format(
                df["customer_name"].nunique()
            ),
            unsafe_allow_html=True,
        )

    with col4:
        total_amount = df["amount"].sum()
        st.markdown(
            """
<div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
           padding: 20px;
           border-radius: 15px;
           color: white;
           text-align: center;">
   <h3>💎</h3>
   <h2>₹{}</h2>
   <p>Total Amount</p>
</div>
""".format(
                total_amount
            ),
            unsafe_allow_html=True,
        )

    # ---------- ALL TRANSACTIONS (NICER TABLE) ----------
    st.markdown("### 📋 All Transactions")

    display_df = df.copy()
    if "timestamp" in display_df.columns:
        display_df["timestamp"] = pd.to_datetime(display_df["timestamp"])

    cols = [c for c in ["timestamp", "customer_name", "item", "type", "amount"] if c in display_df.columns]
    display_df = display_df[cols]

    st.data_editor(
        display_df,
        hide_index=True,
        use_container_width=True,
        key="all_txn_view",
        column_config={
            "timestamp": st.column_config.DatetimeColumn("Time"),
            "customer_name": st.column_config.TextColumn("Customer"),
            "item": st.column_config.TextColumn("Item"),
            "type": st.column_config.TextColumn("Type"),
            "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
        },
        num_rows="fixed",
    )

    # ---------- UDHAAR SUMMARY ----------
    udhaar_df = compute_customer_udhaar(df)
    if udhaar_df is not None and not udhaar_df.empty:
        st.markdown("### 👥 Customer Udhaar Summary")

        tab1, tab2 = st.tabs(["📊 Chart View", "📋 Table View"])

        with tab1:
            # bar chart (can show negative)
            top5_bar = udhaar_df.head(5)

            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]

            bars = ax.bar(
                top5_bar["customer_name"],
                top5_bar["net_udhaar"],
                color=colors[: len(top5_bar)],
                edgecolor="white",
                linewidth=2,
            )

            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"₹{height:.2f}",
                    ha="center",
                    va="bottom",
                    fontweight="bold",
                )

            ax.set_xlabel("Customer", fontsize=12, fontweight="bold")
            ax.set_ylabel("Net Udhaar (₹)", fontsize=12, fontweight="bold")
            ax.set_title("Top Customers by Udhaar", fontsize=14, fontweight="bold")
            ax.set_facecolor("#f8f9fa")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            st.pyplot(fig)

            # pie chart: only positive udhaar to avoid negative wedge error
            positive_udhaar = udhaar_df[udhaar_df["net_udhaar"] > 0].head(5)
            if not positive_udhaar.empty:
                st.markdown("### 📈 Udhaar Distribution (Only positive balances)")
                fig2, ax2 = plt.subplots(figsize=(8, 8))
                ax2.pie(
                    positive_udhaar["net_udhaar"],
                    labels=positive_udhaar["customer_name"],
                    autopct="%1.1f%%",
                    startangle=90,
                )
                ax2.axis("equal")
                st.pyplot(fig2)
            else:
                st.info("All customers are settled or in credit — no positive udhaar to show in the pie chart.")

        with tab2:
            st.data_editor(
                udhaar_df,
                hide_index=True,
                use_container_width=True,
                key="udhaar_table",
                column_config={
                    "customer_name": st.column_config.TextColumn("Customer"),
                    "net_udhaar": st.column_config.NumberColumn(
                        "Net Udhaar (₹)", format="₹%.2f"
                    ),
                },
                num_rows="fixed",
            )
    else:
        st.info("💡 No udhaar/repayment data yet. Start adding udhaars!")

    # ---------- EXCEL-BACKED “DATABASE” VIEW ----------
    st.markdown("### 📒 Transaction Database (Excel)")

    df_excel = load_excel_data()

    if df_excel.empty:
        st.info("No Excel transactions found yet. They will appear here once you start saving transactions.")
        return

    user_id = st.session_state["user_id"]
    df_user = df_excel[df_excel["user_id"] == user_id].copy()

    if df_user.empty:
        st.info("No Excel rows yet for this shop.")
        return

    if "timestamp" in df_user.columns:
        df_user["timestamp"] = pd.to_datetime(df_user["timestamp"])

    st.markdown("#### ✏️ Edit your transaction records")

    edited_df = st.data_editor(
        df_user,
        hide_index=True,
        use_container_width=True,
        key="excel_editor",
        column_config={
            "timestamp": st.column_config.DatetimeColumn("Time"),
            "customer_name": st.column_config.TextColumn("Customer"),
            "item": st.column_config.TextColumn("Item"),
            "type": st.column_config.TextColumn("Type"),
            "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
        },
        num_rows="dynamic",
    )

    if st.button("💾 Save Changes to Excel", use_container_width=True):
        others = df_excel[df_excel["user_id"] != user_id]
        new_full = pd.concat([others, edited_df], ignore_index=True)
        save_excel_data(new_full)
        st.success("✅ Changes saved to Excel!")

    # Profit / Loss Summary from Excel
    summary, _ = calculate_summary(df_user)

    if summary:
        st.markdown("#### 📈 Profit / Loss Summary (from Excel)")

        today = summary.get("today", {})
        week = summary.get("week", {})
        month = summary.get("month", {})

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Today**")
            st.metric("Credit", f"₹{today.get('credit', 0):.2f}")
            st.metric("Debit", f"₹{today.get('debit', 0):.2f}")
            st.metric("Profit", f"₹{today.get('profit', 0):.2f}")

        with col2:
            st.markdown("**Last 7 days**")
            st.metric("Credit", f"₹{week.get('credit', 0):.2f}")
            st.metric("Debit", f"₹{week.get('debit', 0):.2f}")
            st.metric("Profit", f"₹{week.get('profit', 0):.2f}")

        with col3:
            st.markdown("**This Month**")
            st.metric("Credit", f"₹{month.get('credit', 0):.2f}")
            st.metric("Debit", f"₹{month.get('debit', 0):.2f}")
            st.metric("Profit", f"₹{month.get('profit', 0):.2f}")


# ---------------- HOME ----------------
def show_home():
    home_html = """
<div style="text-align: center; padding: 50px 20px;">
   <h1 style="color: #2c3e50; margin-bottom: 30px;">Welcome to SahaYOGI! 🎉</h1>

   <div class="card" style="margin: 20px auto; max-width: 800px;">
       <h2>Your Intelligent Shop Assistant 🤖</h2>
       <p style="font-size: 1.2em; color: #555;">
           Making shop management easy, smart, and efficient for every desi shopkeeper!
       </p>
   </div>

   <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin: 40px 0;">
       <div class="card" style="width: 250px;">
           <h3>🧾 Smart OCR</h3>
           <p>Upload bills and let AI extract items automatically</p>
       </div>
       <div class="card" style="width: 250px;">
           <h3>🎤 Voice Commands</h3>
           <p>Manage udhaar with simple voice/text commands</p>
       </div>
       <div class="card" style="width: 250px;">
           <h3>📊 Live Dashboard</h3>
           <p>Real-time insights and analytics</p>
       </div>
   </div>

   <div style="margin-top: 50px;">
       <h3>Get Started 🚀</h3>
       <p>Login or Register to begin your smart shop journey!</p>
   </div>
</div>
"""
    st.markdown(home_html, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        lottie_url = "https://assets10.lottiefiles.com/packages/lf20_issf4rjp.json"
        animation = load_lottie_url(lottie_url)
        if animation:
            st_lottie(animation, height=200, key="feature1")
        st.markdown(
            "<h4 style='text-align: center;'>Easy Bill Scanning</h4>",
            unsafe_allow_html=True,
        )

    with col2:
        lottie_url = "https://assets8.lottiefiles.com/packages/lf20_xh7zbbbj.json"
        animation = load_lottie_url(lottie_url)
        if animation:
            st_lottie(animation, height=200, key="feature2")
        st.markdown(
            "<h4 style='text-align: center;'>Smart AI Assistant</h4>",
            unsafe_allow_html=True,
        )

    with col3:
        lottie_url = "https://assets7.lottiefiles.com/packages/lf20_2cwDXD.json"
        animation = load_lottie_url(lottie_url)
        if animation:
            st_lottie(animation, height=200, key="feature3")
        st.markdown(
            "<h4 style='text-align: center;'>Live Analytics</h4>",
            unsafe_allow_html=True,
        )


# ---------------- MAIN ----------------
def main():
    st.set_page_config(
        page_title="SahaYOGI",
        page_icon="🛍️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
<style>
.stApp {
   background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
   background-size: 400% 400%;
   animation: gradient 15s.ease infinite;
}
@keyframes gradient {
   0% { background-position: 0% 50%; }
   50% { background-position: 100% 50%; }
   100% { background-position: 0% 50%; }
}
.main-header {
   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   -webkit-background-clip: text;
   -webkit-text-fill-color: transparent;
   text-align: center;
   font-size: 3em !important;
   font-weight: bold;
   margin-bottom: 0.5em;
}
.sidebar-content {
   animation: slideInFromLeft 0.5s.ease-out;
}
@keyframes slideInFromLeft {
   from { transform: translateX(-100%); opacity: 0; }
   to { transform: translateX(0); opacity: 1; }
}
.floating {
   animation: float 6s.ease-in-out infinite;
}
.stButton > button {
   border-radius: 10px !important;
   transition: all 0.3s.ease !important;
}
.stButton > button:hover {
   transform: translateY(-3px) !important;
   box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
}
.card {
   transition: all 0.3s.ease;
   border-radius: 15px;
   padding: 20px;
   background: white;
   box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.card h2, .card h3, .card h4 {
   color: #2c3e50;
   font-weight: 600;
}
.card p {
   color: #333333;
}
.card:hover {
   transform: translateY(-5px);
   box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}
</style>
""",
        unsafe_allow_html=True,
    )

    init_session_state()

    st.markdown(
        '<h1 class="main-header">🛍️ SahaYOGI – Your AI Shop Assistant 🤖</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color: #666;'>Smart Management for Desi Shops 🇮🇳</h3>",
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown(
            """
<div class="sidebar-content">
   <h2 style="text-align: center;">🏪 Navigation</h2>
   <hr style="border: none; height: 2px; background: linear-gradient(90deg, #667eea, #764ba2);">
</div>
""",
            unsafe_allow_html=True,
        )
        lottie_url = "https://assets8.lottiefiles.com/packages/lf20_xh7zbbbj.json"
        animation = load_lottie_url(lottie_url)
        if animation:
            st_lottie(animation, height=150, key="sidebar_animation")

    menu = [
        "🏠 Home",
        "🔐 Login",
        "📝 Register",
        "🧾 Upload Bill",
        "🎤 Command",
        "📊 Dashboard",
        "💬 Chatbot",  # ADDED
    ]
    choice = st.sidebar.selectbox("📱 Menu", menu)

    st.markdown(
        """
<div style="position: fixed; top: 100px; right: 50px; z-index: -1; opacity: 0.3;" class="floating">
   <span style="font-size: 100px;">🛒</span>
</div>
<div style="position: fixed; bottom: 100px; left: 50px; z-index: -1; opacity: 0.3; animation-delay: 2s;" class="floating">
   <span style="font-size: 100px;">💰</span>
</div>
""",
        unsafe_allow_html=True,
    )

    if choice == "🏠 Home":
        show_home()
    elif choice == "🔐 Login":
        show_login()
    elif choice == "📝 Register":
        show_register()
    elif choice == "🧾 Upload Bill":
        show_upload_bill()
    elif choice == "🎤 Command":
        show_voice_command()
    elif choice == "📊 Dashboard":
        show_dashboard()
    elif choice == "💬 Chatbot":  # ADDED
        show_chatbot()


if __name__ == "__main__":
    main()
