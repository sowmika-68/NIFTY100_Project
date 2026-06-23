import pandas as pd
import os

folder = "data"

for file in os.listdir(folder):
    if file.endswith(".xlsx"):
        try:
            df = pd.read_excel(os.path.join(folder, file))
            print("\n" + "="*50)
            print(f"Loaded: {file}")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
        except Exception as e:
            print(f"Error loading {file}: {e}")


from normaliser import normalize_ticker, normalize_year

print(normalize_ticker(" tcs "))
print(normalize_ticker(" infy "))

print(normalize_year(2024.0))
import pandas as pd
from normaliser import normalize_columns

df = pd.read_excel("data/companies.xlsx", header=1)

df = normalize_columns(df)

print(df.columns)
print(df.isnull().sum())