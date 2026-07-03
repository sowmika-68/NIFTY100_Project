"""
Sprint 2 Day 13
Validate Financial Ratios
"""

import sqlite3
import os

DB = "db/nifty100.db"

OUTPUT_DIR = "output"
LOG_FILE = os.path.join(OUTPUT_DIR, "ratio_edge_cases.log")

os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB)
cursor = conn.cursor()

with open(LOG_FILE, "w") as log:

    # Missing Book Value
    cursor.execute("""
    SELECT DISTINCT company_id
    FROM financial_ratios
    WHERE book_value_per_share IS NULL
    """)

    rows = cursor.fetchall()

    log.write("========== BOOK VALUE MISSING ==========\n")

    for row in rows:
        log.write(f"{row[0]}\n")

    # Missing CFO

    cursor.execute("""
    SELECT company_id,year
    FROM financial_ratios
    WHERE cash_from_operations_cr IS NULL
    """)

    rows = cursor.fetchall()

    log.write("\n========== CFO MISSING ==========\n")

    for company, year in rows:
        log.write(f"{company}  {year}\n")

print("Validation Complete")

conn.close()

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
total = cursor.fetchone()[0]

print(f"Total Ratio Records : {total}")

conn.close()