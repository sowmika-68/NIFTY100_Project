"""
Sprint 5 - Day 34

Generate Revenue-Profit Charts
for all companies
"""

import sqlite3
from pathlib import Path

import pandas as pd

from src.reports.charts import revenue_profit_chart

BASE_DIR = Path(__file__).resolve().parents[2]
DB_FILE = BASE_DIR / "db" / "nifty100.db"


def get_companies():

    conn = sqlite3.connect(DB_FILE)

    companies = pd.read_sql(
        """
        SELECT id
        FROM companies
        ORDER BY id
        """,
        conn,
    )

    conn.close()

    return companies


def main():

    print("=" * 50)
    print("GENERATING REVENUE-PROFIT CHARTS")
    print("=" * 50)

    companies = get_companies()

    success = 0
    failed = 0

    for company_id in companies["id"]:

        try:

            revenue_profit_chart(company_id)

            success += 1

            print(f"✓ {company_id}")

        except Exception as e:

            failed += 1

            print(f"✗ {company_id} -> {e}")

    print()
    print("=" * 50)
    print("Completed")
    print("=" * 50)

    print(f"Success : {success}")
    print(f"Failed  : {failed}")


if __name__ == "__main__":
    main()