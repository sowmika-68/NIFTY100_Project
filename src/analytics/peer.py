"""Compute peer percentile rankings and persist to SQLite.

Usage: call `compute_and_populate(peer_excel_path='data/peer_groups.xlsx')`

This script re-uses the ScreenerEngine prepared dataset (latest-year records
with derived CAGR metrics) to compute percentiles within peer groups.
"""

import os
import sqlite3
from typing import Dict

import pandas as pd

from src.screener.engine import ScreenerEngine


METRIC_MAP = {
    "ROE": "return_on_equity_pct",
    "ROCE": "return_on_capital_employed_pct",
    "Net Profit Margin": "net_profit_margin_pct",
    "D/E": "debt_to_equity",
    "FCF": "free_cash_flow_cr",
    "PAT CAGR 5yr": "pat_cagr_5yr",
    "Revenue CAGR 5yr": "revenue_cagr_5yr",
    "EPS CAGR 5yr": "eps_cagr_5yr",
    "Interest Coverage": "interest_coverage",
    "Asset Turnover": "asset_turnover",
}


def percent_rank_series(s: pd.Series) -> pd.Series:
    """Compute percent_rank in range [0,1] using (rank-1)/(n-1).

    Ties use method='min'. If n==1 returns 1.0.
    """
    n = len(s.dropna())
    if n == 0:
        return pd.Series([pd.NA] * len(s), index=s.index)
    if n == 1:
        out = pd.Series(1.0, index=s.index)
        out[s.isna()] = pd.NA
        return out

    ranks = s.rank(method="min", na_option="keep")
    pr = (ranks - 1) / (n - 1)
    pr = pr.where(~s.isna(), other=pd.NA)
    return pr


def compute_and_populate(peer_excel_path: str = "data/peer_groups.xlsx", db_path: str = "db/nifty100.db"):
    if not os.path.exists(peer_excel_path):
        raise FileNotFoundError(f"Peer groups file not found: {peer_excel_path}")

    # Load peer groups workbook: expected sheet with columns company_id, peer_group_name
    df_peers = pd.read_excel(peer_excel_path)
    if "company_id" not in df_peers.columns or "peer_group_name" not in df_peers.columns:
        raise ValueError("peer_groups.xlsx must contain 'company_id' and 'peer_group_name' columns")

    # Prepare screener dataset (latest year + derived metrics)
    engine = ScreenerEngine()
    engine.prepare()
    df = engine.df.copy()

    # Merge peer group info
    df = df.merge(df_peers[["company_id", "peer_group_name"]], on="company_id", how="left")

    # Identify companies without peer group
    missing_pg = df[df["peer_group_name"].isna()]
    if not missing_pg.empty:
        # Print concise message but continue
        print(f"No peer group assigned for {len(missing_pg)} companies; they will be skipped.")

    # Open DB connection and ensure table exists
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS peer_percentiles (
            company_id TEXT,
            peer_group_name TEXT,
            metric TEXT,
            value REAL,
            percentile_rank REAL,
            year TEXT
        )
        """
    )

    # Clear existing entries to avoid duplicates for this run
    cur.execute("DELETE FROM peer_percentiles")

    # Compute percentiles per peer group for the requested metrics
    metrics = list(METRIC_MAP.items())

    rows_to_insert = []
    for pg_name, group_df in df.groupby("peer_group_name"):
        if pd.isna(pg_name):
            continue
        # For each metric compute percent rank inside this peer group
        for metric_label, col in metrics:
            if col not in group_df.columns:
                # If column missing, skip metric for this peer group
                continue

            values = pd.to_numeric(group_df[col], errors="coerce")
            pr = percent_rank_series(values)
            # For D/E invert the percentile so lower D/E => higher rank
            if metric_label == "D/E":
                pr = pr.apply(lambda x: 1.0 - x if pd.notna(x) else pd.NA)

            for idx, row in group_df.iterrows():
                company_id = row["company_id"] if not pd.isna(row["company_id"]) else None
                year = row.get("year")
                value = None
                pr_value = None
                try:
                    value = float(row[col]) if pd.notna(row[col]) else None
                except Exception:
                    value = None
                try:
                    pr_value = float(pr.loc[idx]) if pd.notna(pr.loc[idx]) else None
                except Exception:
                    pr_value = None

                if company_id is None:
                    continue

                rows_to_insert.append((company_id, pg_name, metric_label, value, pr_value, year))

    # Bulk insert
    cur.executemany(
        "INSERT INTO peer_percentiles (company_id, peer_group_name, metric, value, percentile_rank, year) VALUES (?, ?, ?, ?, ?, ?)",
        rows_to_insert,
    )
    conn.commit()
    conn.close()

    print(f"Inserted {len(rows_to_insert)} peer percentile rows into {db_path}.")


if __name__ == "__main__":
    compute_and_populate()
