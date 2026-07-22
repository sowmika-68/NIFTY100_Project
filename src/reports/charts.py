import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"

CHART_DIR = BASE_DIR / "reports" / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Revenue & Profit Chart
# --------------------------------------------------

def revenue_profit_chart(company_id):

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql(
        """
        SELECT
            year,
            sales,
            net_profit
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company_id],
    )

    conn.close()

    if df.empty:
        return None

    plt.figure(figsize=(8, 4))

    plt.bar(
        df["year"],
        df["sales"],
        label="Revenue",
    )

    plt.plot(
        df["year"],
        df["net_profit"],
        marker="o",
        linewidth=2,
        label="Net Profit",
    )

    plt.title(f"{company_id} Revenue vs Net Profit")

    plt.xticks(rotation=45)

    plt.legend()

    plt.tight_layout()

    output_file = CHART_DIR / f"{company_id}_revenue_profit.png"

    plt.savefig(output_file)

    plt.close()

    return output_file


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    file = revenue_profit_chart("TCS")

    print(file)