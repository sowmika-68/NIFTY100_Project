import sqlite3
from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DB_FILE = BASE_DIR / "db" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "reports" / "tearsheets"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Database
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DB_FILE)


# --------------------------------------------------
# Load company details
# --------------------------------------------------

def load_company(company_id):

    conn = get_connection()

    company = pd.read_sql(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        conn,
        params=[company_id],
    )

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company_id],
    )

    profit = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company_id],
    )

    balance = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company_id],
    )

    cashflow = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id=?
        ORDER BY year
        """,
        conn,
        params=[company_id],
    )

    conn.close()
        # Load generated Pros & Cons
    pros_cons = pd.read_csv(
        BASE_DIR / "output" / "pros_cons_generated.csv"
    )

    company_pros = pros_cons[
        (pros_cons["company_id"] == company_id)
        & (pros_cons["type"] == "pro")
    ]

    company_cons = pros_cons[
        (pros_cons["company_id"] == company_id)
        & (pros_cons["type"] == "con")
    ]

    return (
        company,
        ratios,
        profit,
        balance,
        cashflow,
        company_pros,
        company_cons,
    )


# --------------------------------------------------
# Create PDF
# --------------------------------------------------

def create_tearsheet(company_id):

    (
        company,
        ratios,
        profit,
        balance,
        cashflow,
        company_pros,
        company_cons,
    ) = load_company(company_id)
    pros_cons = pd.read_csv(
        BASE_DIR / "output" / "pros_cons_generated.csv"
    )

    company_pros = pros_cons[
        (pros_cons["company_id"] == company_id)
        & (pros_cons["type"] == "pro")
    ]

    company_cons = pros_cons[
        (pros_cons["company_id"] == company_id)
        & (pros_cons["type"] == "con")
    ]

    if company.empty:
        print(f"{company_id} not found.")
        return

    pdf_file = OUTPUT_DIR / f"{company_id}_tearsheet.pdf"

    c = canvas.Canvas(str(pdf_file), pagesize=A4)

    width, height = A4

    # Header
    c.setFillColor(colors.darkblue)
    c.rect(0, height - 55, width, 55, fill=1)

    c.setFillColor(colors.white)

    c.setFont("Helvetica-Bold", 20)

    c.drawString(
        40,
        height - 35,
        company.iloc[0]["company_name"],
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        40,
        height - 52,
        f"Ticker : {company_id}",
    )

    # Placeholder text
    c.setFillColor(colors.black)

    c.setFont("Helvetica-Bold", 16)

    c.drawString(
        40,
        height - 100,
        "Sprint 5 Tearsheet Template",
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        40,
        height - 130,
        f"Profit & Loss Records : {len(profit)}",
    )

    c.drawString(
        40,
        height - 150,
        f"Balance Sheet Records : {len(balance)}",
    )

    c.drawString(
        40,
        height - 170,
        f"Cash Flow Records : {len(cashflow)}",
    )

    c.drawString(
        40,
        height - 190,
        f"Ratio Records : {len(ratios)}",
    )

    # --------------------------------------------------
    # Latest Financial Metrics
    # --------------------------------------------------

    if not ratios.empty:
        latest = ratios.iloc[-1]

        c.setFont("Helvetica-Bold", 13)
        c.drawString(40, height - 220, "Latest Financial Ratios")

        c.setFont("Helvetica", 11)

        roe = latest["return_on_equity_pct"]
        de = latest["debt_to_equity"]
        icr = latest["interest_coverage"]
        fcf = latest["free_cash_flow_cr"]

        c.drawString(
            40,
            height - 240,
            f"ROE : {roe:.2f}%" if pd.notna(roe) else "ROE : N/A"
        )

        c.drawString(
            40,
            height - 258,
            f"Debt / Equity : {de:.2f}" if pd.notna(de) else "Debt / Equity : N/A"
        )

        c.drawString(
            40,
            height - 276,
            f"Interest Coverage : {icr:.2f}" if pd.notna(icr) else "Interest Coverage : N/A"
        )

        c.drawString(
            40,
            height - 294,
            f"FCF : {fcf:.2f} Cr" if pd.notna(fcf) else "FCF : N/A"
        )
    # --------------------------------------------------
    # Revenue vs Profit Chart
    # --------------------------------------------------

    chart_file = (
        BASE_DIR
        / "reports"
        / "charts"
        / f"{company_id}_revenue_profit.png"
    )  

    c.drawImage(
        str(chart_file),
        40,
        20,
        width=500,
        height=240,
        preserveAspectRatio=True,
    )

    # Second Page
    c.showPage()

    c.setFont("Helvetica-Bold", 18)

    c.drawString(
        40,
        800,
        "Key Strengths",
    )

    y = 775

    c.setFont("Helvetica", 11)

    for _, row in company_pros.iterrows():

        c.drawString(
            50,
            y,
            "• " + row["text"],
        )

        y -= 18
        y -= 20

    c.setFont("Helvetica-Bold", 18)

    c.drawString(
        40,
        y,
        "Key Risks",
    )

    y -= 25

    c.setFont("Helvetica", 11)

    for _, row in company_cons.iterrows():

        c.drawString(
            50,
            y,
            "• " + row["text"],
        )

        y -= 18

    c.drawString(
        40,
        770,
        "Charts and Pros/Cons will be added next.",
    )
    from pathlib import Path

    chart_file = (
        BASE_DIR
        / "reports"
        / "charts"
        / f"{company_id}_revenue_profit.png"
    )

    if chart_file.exists():
        c.drawImage(
            str(chart_file),
            50,
            320,
            width=500,
            height=220,
            preserveAspectRatio=True,
        )
    c.save()

    print(f"Created : {pdf_file}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 50)
    print("COMPANY TEARSHEET")
    print("=" * 50)

    create_tearsheet("TCS")

    print("=" * 50)
    print("Day 33 Step 5 Completed")
    print("=" * 50)


if __name__ == "__main__":
    main()