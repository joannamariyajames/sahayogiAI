# analytics.py

import pandas as pd


def transactions_to_dataframe(transactions):
    """
    Convert list of dicts into a Pandas DataFrame.
    """
    if not transactions:
        return pd.DataFrame()
    df = pd.DataFrame(transactions)
    return df


def compute_customer_udhaar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter only udhaar & repayment, then compute net udhaar per customer.
    Positive means customer owes money, negative means they've overpaid.
    """
    if df.empty:
        return df

    if "type" not in df.columns or "amount" not in df.columns:
        return pd.DataFrame()

    df_udhaar = df[df["type"].isin(["udhaar", "repayment"])]
    if df_udhaar.empty:
        return pd.DataFrame()

    summary = df_udhaar.groupby("customer_name")["amount"].sum().reset_index()
    summary = summary.sort_values("amount", ascending=False)
    summary.rename(columns={"amount": "net_udhaar"}, inplace=True)
    return summary
