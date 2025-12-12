import pandas as pd
from datetime import datetime, timedelta
import os

EXCEL_FILE = "transactions.xlsx"

def append_to_excel(user_id, customer_name, item, amount, t_type):
    """
    Appends a new transaction to an Excel sheet.
    Creates the file if it doesn't exist.
    """
    df_new = pd.DataFrame([{
        "timestamp": datetime.now(),
        "user_id": user_id,
        "customer_name": customer_name,
        "item": item,
        "amount": float(amount),
        "type": t_type
    }])

    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_excel(EXCEL_FILE, index=False)


def load_excel_data():
    """Loads the Excel data if exists, else returns empty DataFrame."""
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame(columns=["timestamp", "user_id", "customer_name", "item", "amount", "type"])


def calculate_summary(df):
    """Returns total credit, debit, and profit/loss for day/week/month."""
    if df.empty:
        return {}, df

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    now = datetime.now()
    today = df[df["timestamp"].dt.date == now.date()]
    week = df[df["timestamp"] >= (now - timedelta(days=7))]
    month = df[df["timestamp"].dt.month == now.month]

    def totals(subset):
        credit = subset[subset["amount"] > 0]["amount"].sum()
        debit = subset[subset["amount"] < 0]["amount"].sum()
        profit = credit + debit  # debit is negative
        return {"credit": credit, "debit": abs(debit), "profit": profit}

    return {
        "today": totals(today),
        "week": totals(week),
        "month": totals(month),
    }, df
