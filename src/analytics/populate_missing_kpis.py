"""
Sprint 2 - Day 12
Populate Missing KPI Columns
"""

import sqlite3

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("Updating Book Value Per Share...")

cursor.execute("""
UPDATE financial_ratios
SET book_value_per_share = (
    SELECT companies.book_value
    FROM companies
    WHERE companies.id = financial_ratios.company_id
)
""")

print("Updating Total Debt...")

cursor.execute("""
UPDATE financial_ratios
SET total_debt_cr = (
    SELECT balancesheet.borrowings
    FROM balancesheet
    WHERE balancesheet.company_id = financial_ratios.company_id
    AND balancesheet.year = financial_ratios.year
)
""")

print("Updating Cash From Operations...")

cursor.execute("""
UPDATE financial_ratios
SET cash_from_operations_cr = (
    SELECT cashflow.operating_activity
    FROM cashflow
    WHERE cashflow.company_id = financial_ratios.company_id
    AND cashflow.year = financial_ratios.year
)
""")

conn.commit()

print("Done.")

conn.close()