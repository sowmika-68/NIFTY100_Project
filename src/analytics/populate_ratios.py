"""
Sprint 2 - Day 12

Populate financial_ratios table
"""

import sqlite3

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow_kpis import (
    free_cash_flow,
)

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)

DATABASE = "db/nifty100.db"

connection = sqlite3.connect(DATABASE)

cursor = connection.cursor()

cursor.execute("""
SELECT
    p.company_id,
    p.year,

    p.sales,
    p.operating_profit,
    p.opm_percentage,
    p.other_income,
    p.interest,
    p.net_profit,
    p.eps,
    p.dividend_payout,

    b.equity_capital,
    b.reserves,
    b.borrowings,
    b.investments,
    b.total_assets,

    c.operating_activity,
    c.investing_activity,
    c.financing_activity

FROM profitandloss p

JOIN balancesheet b

ON p.company_id = b.company_id
AND p.year = b.year

JOIN cashflow c

ON p.company_id = c.company_id
AND p.year = c.year
""")

rows = cursor.fetchall()

print(f"Records Loaded : {len(rows)}")

for row in rows:

    (
        company_id,
        year,
        sales,
        operating_profit,
        opm_percentage,
        other_income,
        interest,
        net_profit,
        eps,
        dividend_payout,
        equity_capital,
        reserves,
        borrowings,
        investments,
        total_assets,
        operating_activity,
        investing_activity,
        financing_activity,
    ) = row

    npm = net_profit_margin(net_profit, sales)
    opm = operating_profit_margin(operating_profit, sales, opm_percentage)
    roe = return_on_equity(net_profit, equity_capital, reserves)
    roce = return_on_capital_employed(
        operating_profit,
        equity_capital,
        reserves,
        borrowings,
    )
    roa = return_on_assets(net_profit, total_assets)
    de = debt_to_equity(borrowings, equity_capital, reserves)
    icr = interest_coverage_ratio(
        operating_profit,
        other_income,
        interest,
    )
    turnover = asset_turnover(sales, total_assets)
    fcf = free_cash_flow(
        operating_activity,
        investing_activity,
    )

    # ✅ THIS MUST BE INSIDE THE LOOP
    cursor.execute("""
    INSERT INTO financial_ratios (
        company_id,
        year,
        net_profit_margin_pct,
        operating_profit_margin_pct,
        return_on_equity_pct,
        return_on_capital_employed_pct,
        return_on_assets_pct,
        debt_to_equity,
        interest_coverage,
        asset_turnover,
        free_cash_flow_cr,
        earnings_per_share,
        dividend_payout_ratio_pct
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        company_id,
        year,
        npm,
        opm,
        roe,
        roce,
        roa,
        de,
        icr,
        turnover,
        fcf,
        eps,
        dividend_payout,
    ))

# ✅ THESE STAY OUTSIDE THE LOOP
connection.commit()

print("financial_ratios table populated successfully.")

connection.close()