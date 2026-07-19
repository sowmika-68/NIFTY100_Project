"""
Database utilities for Streamlit dashboard with caching.
All database query functions use @st.cache_data(ttl=600) for performance.
"""

import sqlite3
import re
import pandas as pd
import streamlit as st
import os


DATABASE_PATH = "db/nifty100.db"


def get_connection():
    """Get SQLite database connection."""
    return sqlite3.connect(DATABASE_PATH)


@st.cache_data(ttl=600)
def get_companies():
    """
    Fetch all companies from the database.
    
    Returns:
        pd.DataFrame: Companies data with id, company_name, website, face_value, book_value, roe_percentage
    """
    conn = get_connection()
    query = "SELECT * FROM companies"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    """
    Fetch financial ratios for a company.
    
    Args:
        ticker (str): Company ticker/ID
        year (int, optional): Specific year to filter. If None, returns all years.
    
    Returns:
        pd.DataFrame: Financial ratios data with roe, roce, pe_ratio
    """
    conn = get_connection()
    if year is not None:
        query = """
            SELECT * FROM financial_ratios 
            WHERE company_id = ? AND year = ?
            ORDER BY year DESC
        """
        df = pd.read_sql_query(query, conn, params=(ticker, year))
    else:
        query = """
            SELECT * FROM financial_ratios 
            WHERE company_id = ? 
            ORDER BY year DESC
        """
        df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pl(ticker):
    """
    Fetch profit and loss statement for a company.
    
    Args:
        ticker (str): Company ticker/ID
    
    Returns:
        pd.DataFrame: P&L data with sales, expenses, net_profit by year
    """
    conn = get_connection()
    query = """
        SELECT * FROM profitandloss 
        WHERE company_id = ? 
        ORDER BY year DESC
    """
    df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_bs(ticker):
    """
    Fetch balance sheet for a company.
    
    Args:
        ticker (str): Company ticker/ID
    
    Returns:
        pd.DataFrame: Balance sheet data with total_assets, total_liabilities by year
    """
    conn = get_connection()
    query = """
        SELECT * FROM balancesheet 
        WHERE company_id = ? 
        ORDER BY year DESC
    """
    df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_cf(ticker):
    """
    Fetch cash flow statement for a company.
    
    Args:
        ticker (str): Company ticker/ID
    
    Returns:
        pd.DataFrame: Cash flow data with operating_cash_flow, investing_cash_flow, financing_cash_flow by year
    """
    conn = get_connection()
    query = """
        SELECT * FROM cashflow 
        WHERE company_id = ? 
        ORDER BY year DESC
    """
    df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sectors():
    """
    Fetch all sectors and their companies.
    
    Returns:
        pd.DataFrame: Sector data with company_id and sector_name
    """
    conn = get_connection()
    query = "SELECT * FROM sectors"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peers(group_name):
    """
    Fetch peer companies from a peer group.
    
    Args:
        group_name (str): Peer group name
    
    Returns:
        pd.DataFrame: Peer group data
    """
    conn = get_connection()
    query = """
        SELECT c.*, s.sector_name 
        FROM companies c
        LEFT JOIN sectors s ON c.id = s.company_id
        WHERE s.sector_name = ?
        ORDER BY c.company_name
    """
    df = pd.read_sql_query(query, conn, params=(group_name,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_valuation(ticker):
    """
    Fetch valuation data for a company.
    
    Args:
        ticker (str): Company ticker/ID
    
    Returns:
        pd.DataFrame: Valuation data (if valuation table exists)
    """
    conn = get_connection()
    try:
        query = """
            SELECT * FROM valuation 
            WHERE company_id = ?
        """
        df = pd.read_sql_query(query, conn, params=(ticker,))
    except sqlite3.OperationalError:
        # Valuation table doesn't exist yet
        df = pd.DataFrame()
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_all_tickers():
    """
    Fetch all company tickers/IDs.
    
    Returns:
        list: List of all company IDs
    """
    df = get_companies()
    return sorted(df['id'].tolist())


@st.cache_data(ttl=600)
def get_sector_breakdown():
    """
    Get company count by sector.
    
    Returns:
        pd.DataFrame: Sectors with company counts
    """
    conn = get_connection()
    query = """
        SELECT broad_sector, COUNT(*) as count
        FROM sectors
        GROUP BY broad_sector
        ORDER BY count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_company_details(ticker):
    """
    Get detailed company information.
    
    Args:
        ticker (str): Company ID/ticker
    
    Returns:
        dict: Company details
    """
    conn = get_connection()
    
    # Get basic company info
    query_company = "SELECT * FROM companies WHERE id = ?"
    company = pd.read_sql_query(query_company, conn, params=(ticker,))
    
    # Get sector info
    query_sector = "SELECT broad_sector, sub_sector FROM sectors WHERE company_id = ?"
    sector = pd.read_sql_query(query_sector, conn, params=(ticker,))
    
    conn.close()
    
    result = {}
    if not company.empty:
        result.update(company.iloc[0].to_dict())
    if not sector.empty:
        result.update(sector.iloc[0].to_dict())
    
    return result


@st.cache_data(ttl=600)
def get_market_cap_data(ticker, year=None):
    """
    Get market cap and valuation metrics.
    
    Args:
        ticker (str): Company ticker
        year (int, optional): Specific year
    
    Returns:
        pd.DataFrame: Market cap and valuation data
    """
    conn = get_connection()
    if year:
        query = "SELECT * FROM market_cap WHERE company_id = ? AND year = ?"
        df = pd.read_sql_query(query, conn, params=(ticker, year))
    else:
        query = "SELECT * FROM market_cap WHERE company_id = ? ORDER BY year DESC"
        df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_financial_ratios_full(ticker, year=None):
    """
    Get comprehensive financial ratios.
    
    Returns:
        pd.DataFrame: Full ratios with all metrics
    """
    conn = get_connection()
    if year:
        query = "SELECT * FROM financial_ratios WHERE company_id = ? AND year = ?"
        df = pd.read_sql_query(query, conn, params=(ticker, year))
    else:
        query = "SELECT * FROM financial_ratios WHERE company_id = ? ORDER BY year DESC"
        df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_proscons(ticker):
    """
    Get pros and cons for a company.
    
    Args:
        ticker (str): Company ticker
    
    Returns:
        pd.DataFrame: Pros and cons data
    """
    conn = get_connection()
    query = "SELECT pros, cons FROM prosandcons WHERE company_id = ?"
    df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peer_group_members(group_name):
    """
    Get all members of a peer group.
    
    Args:
        group_name (str): Peer group name
    
    Returns:
        pd.DataFrame: Companies in peer group
    """
    conn = get_connection()
    query = """
        SELECT pg.company_id, c.company_name, s.broad_sector, 
               fr.return_on_equity_pct, fr.debt_to_equity,
               fr.net_profit_margin_pct, fr.free_cash_flow_cr,
               pg.is_benchmark
        FROM peer_groups pg
        LEFT JOIN companies c ON pg.company_id = c.id
        LEFT JOIN sectors s ON pg.company_id = s.company_id
        LEFT JOIN financial_ratios fr ON pg.company_id = fr.company_id 
            AND fr.year = (SELECT MAX(year) FROM financial_ratios WHERE company_id = pg.company_id)
        WHERE pg.peer_group_name = ?
        ORDER BY pg.is_benchmark DESC, c.company_name
    """
    df = pd.read_sql_query(query, conn, params=(group_name,))
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peer_groups_list():
    """
    Get all unique peer group names.
    
    Returns:
        list: List of peer group names
    """
    conn = get_connection()
    query = "SELECT DISTINCT peer_group_name FROM peer_groups ORDER BY peer_group_name"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df['peer_group_name'].tolist()


@st.cache_data(ttl=600)
def get_home_screen_kpis(year=None):
    """
    Get KPI metrics for home screen.
    
    Args:
        year (int, optional): Filter by year
    
    Returns:
        dict: KPI statistics
    """
    conn = get_connection()
    
    # Base query
    year_filter = f"AND year = {year}" if year else ""
    
    # Average ROE
    query_roe = f"SELECT AVG(return_on_equity_pct) FROM financial_ratios WHERE return_on_equity_pct IS NOT NULL {year_filter}"
    avg_roe = pd.read_sql_query(query_roe, conn).iloc[0, 0] or 0
    
    # Median P/E
    query_pe = f"SELECT pe_ratio FROM market_cap WHERE pe_ratio IS NOT NULL {year_filter} ORDER BY pe_ratio"
    pe_data = pd.read_sql_query(query_pe, conn)
    median_pe = pe_data['pe_ratio'].median() if not pe_data.empty else 0
    
    # Median D/E
    query_de = f"SELECT debt_to_equity FROM financial_ratios WHERE debt_to_equity IS NOT NULL {year_filter} ORDER BY debt_to_equity"
    de_data = pd.read_sql_query(query_de, conn)
    median_de = de_data['debt_to_equity'].median() if not de_data.empty else 0
    
    # Total companies
    total_companies = 92
    
    # Median Revenue CAGR (from analysis table)
    query_cagr = "SELECT compounded_sales_growth FROM analysis WHERE compounded_sales_growth IS NOT NULL ORDER BY compounded_sales_growth"
    cagr_data = pd.read_sql_query(query_cagr, conn)
    if not cagr_data.empty:
        # Handle string values like "10 Years: 11%"
        def parse_cagr(val):
            if pd.isna(val) or val is None:
                return None
            if isinstance(val, (int, float)):
                return float(val)
            try:
                match = re.search(r'(\d+\.?\d*)', str(val))
                return float(match.group(1)) if match else None
            except:
                return None
        cagr_data['parsed_cagr'] = cagr_data['compounded_sales_growth'].apply(parse_cagr)
        median_cagr = cagr_data['parsed_cagr'].dropna().median()
        median_cagr = median_cagr if not pd.isna(median_cagr) else 0
    else:
        median_cagr = 0
    
    # Debt-free companies (D/E = 0)
    query_debt_free = f"SELECT COUNT(*) FROM financial_ratios WHERE debt_to_equity = 0 OR debt_to_equity IS NULL {year_filter}"
    debt_free_count = pd.read_sql_query(query_debt_free, conn).iloc[0, 0] or 0
    
    conn.close()
    
    return {
        'avg_roe': round(avg_roe, 2),
        'median_pe': round(median_pe, 2),
        'median_de': round(median_de, 2),
        'total_companies': total_companies,
        'median_revenue_cagr': round(median_cagr, 2),
        'debt_free_count': int(debt_free_count)
    }


@st.cache_data(ttl=600)
def get_company_search_suggestions(search_text):
    """
    Get company suggestions for autocomplete.
    
    Args:
        search_text (str): Search query
    
    Returns:
        list: List of matching companies
    """
    conn = get_connection()
    query = """
        SELECT id, company_name 
        FROM companies 
        WHERE id LIKE ? OR company_name LIKE ?
        ORDER BY company_name
        LIMIT 20
    """
    search_pattern = f"%{search_text}%"
    df = pd.read_sql_query(query, conn, params=(search_pattern, search_pattern))
    conn.close()
    
    # Return list of "TICKER - Company Name" format
    return [f"{row['id']} - {row['company_name']}" for _, row in df.iterrows()]


@st.cache_data(ttl=600)
def get_screener_data(year=None):
    """
    Get all companies with key metrics for screener.
    
    Returns:
        pd.DataFrame: Companies with all screening metrics
    """
    conn = get_connection()
    
    year_filter = f"AND fr.year = {year}" if year else ""
    
    query = f"""
        SELECT 
            c.id,
            c.company_name,
            s.broad_sector,
            fr.return_on_equity_pct as roe,
            fr.debt_to_equity as de,
            fr.free_cash_flow_cr as fcf,
            a.compounded_sales_growth as revenue_cagr,
            a.compounded_profit_growth as pat_cagr,
            fr.operating_profit_margin_pct as opm,
            m.pe_ratio,
            m.pb_ratio,
            m.dividend_yield_pct as div_yield,
            fr.interest_coverage as icr,
            (fr.return_on_equity_pct * 0.3 + 
             (100 - fr.debt_to_equity) * 0.2 + 
             fr.operating_profit_margin_pct * 0.2 +
             (m.pe_ratio / 30) * 0.15 +
             fr.interest_coverage * 0.15) as composite_score
        FROM companies c
        LEFT JOIN sectors s ON c.id = s.company_id
        LEFT JOIN financial_ratios fr ON c.id = fr.company_id
        LEFT JOIN analysis a
        ON c.id = a.company_id

        LEFT JOIN market_cap m
        ON c.id = m.company_id
        AND m.year = (
            SELECT MAX(year)
            FROM market_cap
            WHERE company_id = c.id
        )
        
        WHERE fr.year = (
            SELECT MAX(year)
            FROM financial_ratios
            WHERE company_id = c.id
        )

        AND a.id = (
            SELECT MAX(id)
            FROM analysis
            WHERE company_id = c.id
        ) {year_filter}
        ORDER BY composite_score DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert CAGR text to numeric values
    def extract_percent(value):
        if pd.isna(value):
            return None

        value = str(value)

        import re
        match = re.search(r'(\d+(\.\d+)?)', value)
    
        if match:
            return float(match.group(1))

        return None


    df["revenue_cagr"] = df["revenue_cagr"].apply(extract_percent)
    df["pat_cagr"] = df["pat_cagr"].apply(extract_percent)

    return df
@st.cache_data(ttl=600)
def get_sector_analysis_data():
    """
    Get all companies with sector, ROE and market cap data
    for Sector Analysis page.
    """
    conn = get_connection()

    query = """
SELECT
    c.id,
    c.company_name,
    s.broad_sector,
    s.sub_sector,
    fr.return_on_equity_pct,
    m.market_cap_crore,
    p.sales
FROM companies c
LEFT JOIN sectors s
    ON c.id = s.company_id
LEFT JOIN financial_ratios fr
    ON c.id = fr.company_id
LEFT JOIN market_cap m
    ON c.id = m.company_id
    AND m.year = (
        SELECT MAX(year)
        FROM market_cap
        WHERE company_id = c.id
    )
LEFT JOIN profitandloss p
    ON c.id = p.company_id
    AND p.year = (
        SELECT MAX(year)
        FROM profitandloss
        WHERE company_id = c.id
    )
WHERE fr.year = (
    SELECT MAX(year)
    FROM financial_ratios
    WHERE company_id = c.id
)
"""

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_annual_reports(ticker):
    """
    Fetch annual reports for a company.
    """
    conn = get_connection()

    query = """
        SELECT
            Year,
            Annual_Report
        FROM documents
        WHERE company_id = ?
        ORDER BY Year DESC
    """

    df = pd.read_sql_query(query, conn, params=(ticker,))
    conn.close()

    return df
@st.cache_data(ttl=600)
def get_valuation_data():
    """
    Return latest valuation metrics for all companies.
    """

    conn = get_connection()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        mc.market_cap_crore,
        mc.pe_ratio,
        fr.free_cash_flow_cr,

        (fr.free_cash_flow_cr * 100.0 /
            mc.market_cap_crore) AS fcf_yield,

        (100.0 /
            mc.pe_ratio) AS earnings_yield

    FROM companies c

    LEFT JOIN sectors s
        ON c.id=s.company_id

    LEFT JOIN market_cap mc
        ON c.id=mc.company_id

    LEFT JOIN financial_ratios fr
        ON c.id=fr.company_id

    WHERE mc.year=(
        SELECT MAX(year)
        FROM market_cap m2
        WHERE m2.company_id=c.id
    )

    AND fr.year=(
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id=c.id
    )

    ORDER BY c.company_name
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df
@st.cache_data(ttl=600)
def get_valuation_data():
    """
    Load valuation summary generated by valuation.py
    """

    from pathlib import Path
    import pandas as pd

    base_dir = Path(__file__).resolve().parents[3]
    file_path = base_dir / "output" / "valuation_summary.xlsx"

    if file_path.exists():
        return pd.read_excel(file_path)

    return pd.DataFrame()