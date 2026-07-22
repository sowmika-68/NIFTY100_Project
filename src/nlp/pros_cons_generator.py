import sqlite3
from pathlib import Path

import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# Load data
# --------------------------------------------------
def load_data():
    """
    Load companies and financial ratios from SQLite.
    """

    conn = sqlite3.connect(DB_FILE)

    # Load companies
    companies_df = pd.read_sql(
        """
        SELECT
            id AS company_id,
            company_name
        FROM companies
        ORDER BY id
        """,
        conn,
    )

    # Load financial ratios
    ratios_df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        ORDER BY company_id, year
        """,
        conn,
    )

    conn.close()

    return companies_df, ratios_df


# --------------------------------------------------
# Generate Pros
# --------------------------------------------------
def generate_pros(company_id, company_data):
    """
    Generate all Pro statements for a company.
    """

    pros = []

    # Get latest financial year
    latest = company_data.sort_values("year").iloc[-1]

    # -----------------------------
    # PRO_01 : ROE > 20%
    # -----------------------------
    if (
        pd.notna(latest["return_on_equity_pct"])
        and latest["return_on_equity_pct"] > 20
    ):
        pros.append(
            {
                "company_id": company_id,
                "type": "pro",
                "rule_id": "PRO_01",
                "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",
                "confidence_pct": calculate_confidence("PRO_01"),
            }
        )

    # -----------------------------
    # PRO_02 : Debt Free
    # -----------------------------
    if (
        pd.notna(latest["debt_to_equity"])
        and latest["debt_to_equity"] == 0
    ):
        pros.append(
            {
                "company_id": company_id,
                "type": "pro",
                "rule_id": "PRO_02",
                "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden",
                "confidence_pct": calculate_confidence("PRO_01"),
            }
        )

    # -----------------------------
    # PRO_03 : OPM > 25%
    # -----------------------------
    if (
        pd.notna(latest["operating_profit_margin_pct"])
        and latest["operating_profit_margin_pct"] > 25
    ):
        pros.append(
            {
                "company_id": company_id,
                "type": "pro",
                "rule_id": "PRO_03",
                "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline",
                "confidence_pct": calculate_confidence("PRO_01"),
                
            }
        )

    # -----------------------------
    # PRO_04 : Interest Coverage > 10
    # -----------------------------
    if (
        pd.notna(latest["interest_coverage"])
        and latest["interest_coverage"] > 10
    ):
        pros.append(
            {
                "company_id": company_id,
                "type": "pro",
                "rule_id": "PRO_04",
                "text": "Very high interest coverage ratio reflects negligible financial stress from debt servicing",
                "confidence_pct": calculate_confidence("PRO_01"),
            }
        )

    # -----------------------------
    # PRO_05 : Positive Free Cash Flow
    # -----------------------------
    if (
        pd.notna(latest["free_cash_flow_cr"])
        and latest["free_cash_flow_cr"] > 0
    ):
        pros.append(
            {
                "company_id": company_id,
                "type": "pro",
                "rule_id": "PRO_05",
                "text": "Strong free cash flow generation signals healthy business fundamentals",
                "confidence_pct": calculate_confidence("PRO_01"),
            }
        )

    return pros


# --------------------------------------------------
# Generate Cons
# --------------------------------------------------
def generate_cons(company_id, company_data):
    """
    Generate all Con statements for a company.
    """

    cons = []

    # Get latest financial year
    latest = company_data.sort_values("year").iloc[-1]

    # -----------------------------
    # CON_01 : Debt/Equity > 2
    # -----------------------------
    if (
        pd.notna(latest["debt_to_equity"])
        and latest["debt_to_equity"] > 2
    ):
        cons.append(
            {
                "company_id": company_id,
                "type": "con",
                "rule_id": "CON_01",
                "text": f"Debt-to-equity ratio of {latest['debt_to_equity']:.2f} is elevated for a non-financial company and warrants monitoring.",
                "confidence_pct": calculate_confidence("CON_02"),
            }
        )

    # -----------------------------
    # CON_02 : Interest Coverage < 1.5
    # -----------------------------
    if (
        pd.notna(latest["interest_coverage"])
        and latest["interest_coverage"] < 1.5
    ):
        cons.append(
            {
                "company_id": company_id,
                "type": "con",
                "rule_id": "CON_02",
                "text": "Interest coverage ratio below 1.5x indicates the company may struggle to meet debt obligations.",
                "confidence_pct": calculate_confidence("CON_02"),
            }
        )

    # -----------------------------
    # CON_03 : OPM < 10
    # -----------------------------
    if (
        pd.notna(latest["operating_profit_margin_pct"])
        and latest["operating_profit_margin_pct"] < 10
    ):
        cons.append(
            {
                "company_id": company_id,
                "type": "con",
                "rule_id": "CON_03",
                "text": "Operating margins are relatively low and may indicate pricing or cost pressure.",
                "confidence_pct": calculate_confidence("CON_02"),
            }
        )

    # -----------------------------
    # CON_04 : ROE < 10
    # -----------------------------
    if (
        pd.notna(latest["return_on_equity_pct"])
        and latest["return_on_equity_pct"] < 10
    ):
        cons.append(
            {
                "company_id": company_id,
                "type": "con",
                "rule_id": "CON_04",
                "text": "Return on equity below 10% suggests weak shareholder returns.",
                "confidence_pct": calculate_confidence("CON_02"),
            }
        )

    # -----------------------------
    # CON_05 : Negative Free Cash Flow
    # -----------------------------
    if (
        pd.notna(latest["free_cash_flow_cr"])
        and latest["free_cash_flow_cr"] < 0
    ):
        cons.append(
            {
                "company_id": company_id,
                "type": "con",
                "rule_id": "CON_05",
                "text": "Negative free cash flow raises concerns about cash generation quality.",
                "confidence_pct": calculate_confidence("CON_02"),
            }
        )

    return cons


# --------------------------------------------------
# Calculate Confidence
# --------------------------------------------------
def calculate_confidence(rule_id):
    """
    Return confidence score based on rule.
    """

    confidence_map = {
        "PRO_01": 95,
        "PRO_02": 95,
        "PRO_03": 90,
        "PRO_04": 90,
        "PRO_05": 85,

        "CON_01": 95,
        "CON_02": 90,
        "CON_03": 85,
        "CON_04": 80,
        "CON_05": 85,
    }

    return confidence_map.get(rule_id, 65)


# --------------------------------------------------
# Save Output
# --------------------------------------------------
def save_output(df):
    """
    Save the generated Pros & Cons to CSV.
    """

    output_file = OUTPUT_DIR / "pros_cons_generated.csv"

    df.to_csv(output_file, index=False)

    print("\nOutput Saved Successfully!")
    print(f"File : {output_file}")


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():

    print("=" * 50)
    print("NLP PROS & CONS GENERATOR")
    print("=" * 50)

    companies_df, ratios_df = load_data()

    all_results = []

    for _, company in companies_df.iterrows():

        company_id = company["company_id"]

        company_data = ratios_df[
            ratios_df["company_id"] == company_id
        ]

        if company_data.empty:
            all_results.append(
                {
                    "company_id": company_id,
                    "type": "pro",
                    "rule_id": "PRO_DEFAULT",
                    "text": "Financial ratio data unavailable. Detailed evaluation pending.",
                    "confidence_pct": 65,
                }
            )

            all_results.append(
                {
                    "company_id": company_id,
                    "type": "con",
                    "rule_id": "CON_DEFAULT",
                    "text": "Financial ratio data unavailable for rule evaluation.",
                    "confidence_pct": 65,
                }
            )

            continue
            

        pros = generate_pros(company_id, company_data)
        cons = generate_cons(company_id, company_data)

        # Ensure at least one Pro
        if not pros:
            pros.append(
                {
                    "company_id": company_id,
                    "type": "pro",
                    "rule_id": "PRO_DEFAULT",
                    "text": "Company demonstrates stable financial characteristics requiring further evaluation.",
                    "confidence_pct": 65,
                }
            )

        # Ensure at least one Con
        if not cons:
            cons.append(
                {
                    "company_id": company_id,
                    "type": "con",
                    "rule_id": "CON_DEFAULT",
                    "text": "No major financial weakness detected by current rule set. Continued monitoring is recommended.",
                    "confidence_pct": 65,
                }
            )

        all_results.extend(pros)
        all_results.extend(cons)

    output_df = pd.DataFrame(all_results)

    save_output(output_df)

    print()
    print(f"Companies Processed : {len(companies_df)}")
    print(f"Records Generated : {len(output_df)}")

    print("=" * 50)
    print("Day 30 completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()