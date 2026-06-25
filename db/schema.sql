CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    company_name TEXT,
    website TEXT,
    face_value REAL,
    book_value REAL,
    roe_percentage REAL
);

CREATE TABLE IF NOT EXISTS profitandloss (
    company_id TEXT,
    year INTEGER,
    sales REAL,
    expenses REAL,
    net_profit REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS balancesheet (
    company_id TEXT,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS cashflow (
    company_id TEXT,
    year INTEGER,
    operating_cash_flow REAL,
    investing_cash_flow REAL,
    financing_cash_flow REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    company_id TEXT,
    year INTEGER,
    roe REAL,
    roce REAL,
    pe_ratio REAL,

    PRIMARY KEY(company_id, year),

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS stock_prices (
    company_id TEXT,
    price_date TEXT,
    close_price REAL,

    PRIMARY KEY(company_id, price_date),

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS stock_prices (
    company_id TEXT,
    price_date TEXT,
    close_price REAL,

    PRIMARY KEY(company_id, price_date),

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS sectors (
    company_id TEXT,
    sector_name TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS analysis (
    company_id TEXT,
    remarks TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS documents (
    company_id TEXT,
    document_link TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS prosandcons (
    company_id TEXT,
    pros TEXT,
    cons TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS peer_groups (
    company_id TEXT,
    peer_company TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);