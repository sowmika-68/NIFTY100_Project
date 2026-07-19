import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)
def get_connection():
    return sqlite3.connect(DB_PATH)
def load_data():
    """
    Load all tables required for valuation.
    """

    conn = get_connection()

    companies = pd.read_sql_query(
        "SELECT * FROM companies",
        conn
    )

    sectors = pd.read_sql_query(
        "SELECT * FROM sectors",
        conn
    )

    market_cap = pd.read_sql_query(
        "SELECT * FROM market_cap",
        conn
    )

    financial_ratios = pd.read_sql_query(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return companies, sectors, market_cap, financial_ratios
def prepare_latest_data():

    companies, sectors, market_cap, financial_ratios = load_data()

    # Latest Market Cap record
    market_cap = (
        market_cap.sort_values("year")
        .groupby("company_id", as_index=False)
        .last()
    )

    # Latest Financial Ratio record
    # Extract the 4-digit year from values like "Dec 2023"
    financial_ratios["year"] = (
        financial_ratios["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
        .astype(int)
    )

    financial_ratios = (
        financial_ratios.sort_values("year")
        .groupby("company_id", as_index=False)
        .last()
    )
    # Remove unnecessary id columns before merging
    if "id" in sectors.columns:
        sectors = sectors.drop(columns=["id"])

    if "id" in market_cap.columns:
        market_cap = market_cap.drop(columns=["id"])

    if "id" in financial_ratios.columns:
        financial_ratios = financial_ratios.drop(columns=["id"])

    return companies, sectors, market_cap, financial_ratios
def build_master_dataframe():

    companies, sectors, market_cap, financial_ratios = prepare_latest_data()

    df = companies.merge(
        sectors,
        left_on="id",
        right_on="company_id",
        how="left"
    )

    df = df.merge(
        market_cap,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("", "_mc")
    )

    df = df.merge(
        financial_ratios,
        left_on="id",
        right_on="company_id",
        how="left",
        suffixes=("", "_fr")
    )

    return df
def calculate_valuation(df):
    """
    Calculate valuation metrics.
    """

    # Avoid divide by zero
    df["fcf_yield"] = (
        df["free_cash_flow_cr"] /
        df["market_cap_crore"]
    ) * 100

    df["earnings_yield"] = (
        100 / df["pe_ratio"]
    )

    # Valuation Label

    conditions = [
        df["pe_ratio"] < 20,
        (df["pe_ratio"] >= 20) & (df["pe_ratio"] <= 35),
        df["pe_ratio"] > 35
    ]

    labels = [
        "Undervalued",
        "Fairly Valued",
        "Overvalued"
    ]

    import numpy as np

    df["valuation"] = np.select(
        conditions,
        labels,
        default="Unknown"
    )

    return df
def export_valuation(df):
    """
    Export valuation report to Excel.
    """

    output_file = OUTPUT_DIR / "valuation_summary.xlsx"

    columns = [
        "id",
        "company_name",
        "broad_sector",
        "market_cap_crore",
        "pe_ratio",
        "fcf_yield",
        "earnings_yield",
        "valuation"
    ]

    export_df = df[columns].copy()

    export_df.columns = [
        "Ticker",
        "Company",
        "Sector",
        "Market Cap (Cr)",
        "P/E",
        "FCF Yield %",
        "Earnings Yield %",
        "Valuation"
    ]

    export_df.to_excel(
        output_file,
        index=False
    )

    print("\n===================================")
    print("Valuation report exported.")
    print(output_file)
    print("===================================")
if __name__ == "__main__":

    df = build_master_dataframe()

    df = calculate_valuation(df)

    export_valuation(df)

    print(df.head())