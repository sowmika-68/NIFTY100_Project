import re
import sqlite3
from pathlib import Path

import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

ANALYSIS_FILE = BASE_DIR / 'data' / 'analysis.xlsx'
DB_FILE = BASE_DIR / 'db' / 'nifty100.db'
OUTPUT_DIR = BASE_DIR / 'output'

OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Regex pattern
# Handles:
#   10 Years: 21%
#   5 Years 18%
#   1 Year: -2%
#   Last Year: 12%
# --------------------------------------------------
PATTERN = re.compile(
    r"(?:(Last\s+Year)|(\d+)\s*Years?)\s*:?\s*(-?[\d.]+)\s*%",
    re.IGNORECASE,
)

# --------------------------------------------------
# Load analysis data
# --------------------------------------------------
def load_analysis_data():
    df = pd.read_excel(ANALYSIS_FILE, header=1)

    # Keep only required columns
    df = df[
        [
            'company_id',
            'compounded_sales_growth',
            'compounded_profit_growth',
            'stock_price_cagr',
            'roe',
        ]
    ].copy()

    return df


# --------------------------------------------------
# Parse a single text field
# --------------------------------------------------
def parse_metric(text):
    if pd.isna(text):
        return None

    text = str(text).strip()

    # collapse multiple spaces into one
    text = " ".join(text.split())

    match = PATTERN.search(text)

    if not match:
        return None

    last_year = match.group(1)
    period = match.group(2)
    value_text = match.group(3)

    if last_year:
        period_years = 1
    else:
        period_years = int(period)

    value_pct = float(value_text)

    return period_years, value_pct


# --------------------------------------------------
# Extract metrics
# --------------------------------------------------
def extract_metrics(df):
    metric_columns = [
        'compounded_sales_growth',
        'compounded_profit_growth',
        'stock_price_cagr',
        'roe',
    ]

    parsed_rows = []
    failure_rows = []

    for _, row in df.iterrows():
        company_id = row['company_id']

        for metric in metric_columns:
            raw_text = row[metric]

            result = parse_metric(raw_text)

            if result is None:
                failure_rows.append(
                    {
                        'company_id': company_id,
                        'metric_type': metric,
                        'original_text': raw_text,
                        'reason': 'Regex not matched',
                    }
                )
                continue

            period_years, value_pct = result

            parsed_rows.append(
                {
                    'company_id': company_id,
                    'metric_type': metric,
                    'period_years': period_years,
                    'value_pct': value_pct,
                }
            )

    parsed_df = pd.DataFrame(parsed_rows)
    failures_df = pd.DataFrame(failure_rows)

    return parsed_df, failures_df


# --------------------------------------------------
# Validation against Ratio Engine
# Current DB does not contain CAGR columns
# --------------------------------------------------
def validate_against_ratios(parsed_df):
    conn = sqlite3.connect(DB_FILE)

    ratios_df = pd.read_sql('SELECT * FROM financial_ratios LIMIT 1', conn)

    conn.close()

    validation_rows = []

    required_cols = {'revenue_cagr_5yr', 'pat_cagr_5yr'}

    if not required_cols.issubset(ratios_df.columns):
        validation_rows.append(
            {
                'company_id': 'ALL',
                'metric_type': 'CAGR_VALIDATION',
                'parsed_value': None,
                'computed_value': None,
                'difference_pct': None,
                'status': 'SKIPPED - CAGR columns not available in financial_ratios',
            }
        )

        validation_df = pd.DataFrame(validation_rows)

        validation_df.to_csv(
            OUTPUT_DIR / 'cagr_validation.csv',
            index=False,
        )

        return validation_df

    # Future implementation placeholder
    validation_df = pd.DataFrame(validation_rows)

    validation_df.to_csv(
        OUTPUT_DIR / 'cagr_validation.csv',
        index=False,
    )

    return validation_df


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    print('=' * 50)
    print('NLP ANALYSIS PARSER')
    print('=' * 50)

    df = load_analysis_data()

    parsed_df, failures_df = extract_metrics(df)

    # Save parsed data
    parsed_file = OUTPUT_DIR / 'analysis_parsed.csv'
    parsed_df.to_csv(parsed_file, index=False)

    # Save failures
    failures_file = OUTPUT_DIR / 'parse_failures.csv'
    failures_df.to_csv(failures_file, index=False)

    # Validation
    validation_df = validate_against_ratios(parsed_df)

    print(f'Companies Processed : {df["company_id"].nunique()}')
    print(f'Metrics Parsed      : {len(parsed_df)}')
    print(f'Parse Failures      : {len(failures_df)}')
    print(f'Validation Rows     : {len(validation_df)}')

    print('\\nFiles Generated:')
    print(f'  - {parsed_file}')
    print(f'  - {failures_file}')
    print(f'  - {OUTPUT_DIR / "cagr_validation.csv"}')

    print('\\nDay 29 completed successfully!')
    print('=' * 50)


if __name__ == '__main__':
    main()