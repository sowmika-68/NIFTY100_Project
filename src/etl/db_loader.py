import pandas as pd
import sqlite3
import os
conn = sqlite3.connect("db/nifty100.db")

print("Database Connected")

files = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "market_cap": "market_cap.xlsx"
}

load_audit = []

for table_name, file_name in files.items():

    path = os.path.join("data", file_name)

    try:

        df = pd.read_excel(path, header=1)

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"{table_name} loaded")

        load_audit.append(
            [table_name, len(df), "SUCCESS"]
        )

    except Exception as e:

        print(e)

        load_audit.append(
            [table_name, 0, "FAILED"]
        )

audit_df = pd.DataFrame(
    load_audit,
    columns=[
        "table_name",
        "row_count",
        "status"
    ]
)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print("Audit File Created")

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

print(cursor.fetchall())

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "stock_prices"
]

for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(table, count)

conn.commit()
conn.close()

print("Database Closed")