import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type='table'
""", conn)

print("\nTABLES")
print(tables)

for table in tables["name"]:
    count = pd.read_sql(
        f"SELECT COUNT(*) as rows FROM {table}",
        conn
    )
    print(f"\n{table}")
    print(count)

conn.close()