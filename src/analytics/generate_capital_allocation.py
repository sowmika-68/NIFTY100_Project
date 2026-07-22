import csv
import sqlite3
from pathlib import Path

from src.analytics.cashflow_kpis import capital_allocation_pattern

BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"

OUTPUT_FILE = BASE_DIR / "output" / "capital_allocation.csv"


def main():

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company_id,
            year,
            operating_activity,
            investing_activity,
            financing_activity
        FROM cashflow
        ORDER BY company_id, year
    """)

    rows = cursor.fetchall()

    conn.close()

    with open(OUTPUT_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "company_id",
                "year",
                "cfo_sign",
                "cfi_sign",
                "cff_sign",
                "pattern_label",
            ]
        )

        for row in rows:

            company_id = row[0]
            year = row[1]

            cfo = row[2] if row[2] is not None else 0
            cfi = row[3] if row[3] is not None else 0
            cff = row[4] if row[4] is not None else 0
            
            cfo_sign, cfi_sign, cff_sign, label = (
                capital_allocation_pattern(
                    cfo,
                    cfi,
                    cff,
                )
            )

            writer.writerow(
                [
                    company_id,
                    year,
                    cfo_sign,
                    cfi_sign,
                    cff_sign,
                    label,
                ]
            )

    print("=" * 50)
    print("Capital Allocation Report Generated")
    print("=" * 50)
    print(f"Rows Written : {len(rows)}")
    print(f"Output File  : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()