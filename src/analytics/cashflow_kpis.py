"""
Sprint 2 - Day 11

Cash Flow KPI Engine
"""

from typing import Optional


def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Calculate Free Cash Flow.

    If either value is missing,
    return None.
    """

    if operating_activity is None:
        return None

    if investing_activity is None:
        return None

    return operating_activity + investing_activity


def cfo_quality_score(cfo_total: float, pat_total: float):
    """
    Calculate CFO Quality Score.

    Ratio = CFO / PAT
    """

    if pat_total == 0:
        return None

    ratio = cfo_total / pat_total

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity: float, sales: float):
    """
    Calculate CapEx Intensity.
    """

    if sales == 0:
        return None

    value = (abs(investing_activity) / sales) * 100

    if value < 3:
        category = "Asset Light"

    elif value <= 8:
        category = "Moderate"

    else:
        category = "Capital Intensive"

    return round(value, 2), category


def fcf_conversion_rate(
    free_cash_flow: float, operating_profit: float
) -> Optional[float]:
    """
    Calculate FCF Conversion Rate.
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100


def capital_allocation_pattern(
    cfo: float, cfi: float, cff: float, cfo_pat_ratio: float = None
):
    """
    Classify capital allocation pattern based on
    CFO, CFI and CFF signs.
    """

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Unknown"

    return (cfo_sign, cfi_sign, cff_sign, label)


import sqlite3
from pathlib import Path

import pandas as pd
# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)
def load_data():

    conn = sqlite3.connect(DB_FILE)

    cashflow_df = pd.read_sql(
        "SELECT * FROM cashflow",
        conn,
    )

    ratios_df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    companies_df = pd.read_sql(
        "SELECT * FROM companies",
        conn,
    )

    conn.close()

    return cashflow_df, ratios_df, companies_df

def detect_distress(df):
    """
    Add distress flag.
    """

    df["distress_flag"] = (
        (df["cfo_quality"] < 0)
        & (df["debt_to_equity"] > 1)
    )

    return df

def save_reports(df):

    excel_file = OUTPUT_DIR / "cashflow_intelligence.xlsx"
    csv_file = OUTPUT_DIR / "distress_alerts.csv"

    df.to_excel(excel_file, index=False)

    distress = df[df["distress_flag"]]

    distress.to_csv(csv_file, index=False)

    print()
    print("Reports Generated Successfully")
    print(excel_file)
    print(csv_file)

def generate_cashflow_intelligence():
    """
    Generate Cash Flow Intelligence report.
    """

    cashflow_df, ratios_df, companies_df = load_data()

    results = []

    for company_id in cashflow_df["company_id"].unique():

        company_cash = cashflow_df[
            cashflow_df["company_id"] == company_id
        ].copy()

        company_ratio = ratios_df[
            ratios_df["company_id"] == company_id
        ].copy()

        if company_cash.empty or company_ratio.empty:
            continue

        company_cash = company_cash.sort_values("year")
        company_ratio = company_ratio.sort_values("year")

        latest_cash = company_cash.iloc[-1]
        latest_ratio = company_ratio.iloc[-1]

        results.append(
            {
                "company_id": company_id,
                "cfo_quality": latest_ratio["cash_from_operations_cr"],
                "free_cash_flow": latest_ratio["free_cash_flow_cr"],
                "capex": latest_ratio["capex_cr"],
                "debt_to_equity": latest_ratio["debt_to_equity"],
            }
        )

    return pd.DataFrame(results)

def main():

    print("=" * 50)
    print("CASH FLOW INTELLIGENCE")
    print("=" * 50)

    df = generate_cashflow_intelligence()

    df = detect_distress(df)

    save_reports(df)

    print()
    print("Companies :", len(df))

    print("=" * 50)
    print("Day 31 Completed Successfully")
    print("=" * 50)


if __name__ == "__main__":
    main()