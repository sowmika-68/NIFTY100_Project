import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT COUNT(*) as total_companies
FROM companies
"""

df = pd.read_sql(query, conn)

print(df)

import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT *
FROM companies
ORDER BY RANDOM()
LIMIT 5
"""

df = pd.read_sql(query, conn)

print(df)


import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT *
FROM profitandloss
LIMIT 5
"""

df = pd.read_sql(query, conn)

print(df.columns)
print(df.head())

import pandas as pd

df = pd.read_excel(
    "data/profitandloss.xlsx",
    header=None
)

print(df.head(10))

pd.read_excel(
    "data/profitandloss.xlsx",
    header=1
)

import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT company_id,
COUNT(DISTINCT year) as total_years
FROM profitandloss
GROUP BY company_id
ORDER BY total_years
"""

df = pd.read_sql(query, conn)

print(df.head(20))

import pandas as pd

df = pd.read_csv("output/load_audit.csv")
print(df)

import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT *
FROM companies
ORDER BY RANDOM()
LIMIT 5
"""

df = pd.read_sql(query, conn)

print(df[['id']])


import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT *
FROM profitandloss
WHERE company_id='TORNTPHARM'
"""

df = pd.read_sql(query, conn)

print(df.head())