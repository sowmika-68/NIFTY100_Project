"""Generate radar charts per company within peer groups.

Exports PNGs to `reports/radar_charts/<company_id>_radar.png`.

Behavior:
- Uses ScreenerEngine.prepare() to get latest-year dataset with derived metrics.
- Loads `data/peer_groups.xlsx` with columns `company_id` and `peer_group_name`.
- Metrics (axes): ROE, ROCE, NPM, D/E (inverted), FCF (free_cash_flow_cr), PAT CAGR 5yr,
  Revenue CAGR 5yr, Composite Score.
- Values are percentile-ranked within the peer group (0-100). D/E percentile is inverted
  so lower D/E gives higher score.
- Plots company's polygon (filled) and peer-group average as dashed outline.
- For companies without peer group: creates a single-axis chart for Composite Score vs
  Nifty 100 average.
"""

import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.screener.engine import ScreenerEngine


AXES = [
    ("ROE", "return_on_equity_pct"),
    ("ROCE", "return_on_capital_employed_pct"),
    ("NPM", "net_profit_margin_pct"),
    ("D/E", "debt_to_equity"),
    ("FCF", "free_cash_flow_cr"),
    ("PAT CAGR 5yr", "pat_cagr_5yr"),
    ("Revenue CAGR 5yr", "revenue_cagr_5yr"),
    ("Composite", "composite_quality_score"),
]


def percent_rank_series(s: pd.Series) -> pd.Series:
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


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def draw_radar(company_id: str, company_values: List[float], peer_avg: List[float], axes_labels: List[str], out_path: str):
    # number of variables
    N = len(axes_labels)

    # angles
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    # close the plot
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # labels
    plt.xticks(angles[:-1], axes_labels, fontsize=10)

    # radial ticks
    ax.set_rlabel_position(30)
    plt.yticks([0.25, 0.5, 0.75], ["25", "50", "75"], color="grey", size=8)
    plt.ylim(0, 1)

    # company polygon
    vals = [v if (v is not None and not pd.isna(v)) else 0.0 for v in company_values]
    vals += vals[:1]
    ax.plot(angles, vals, color="#1f77b4", linewidth=2)
    ax.fill(angles, vals, color="#1f77b4", alpha=0.25)

    # peer average dashed outline
    avg_vals = [v if (v is not None and not pd.isna(v)) else 0.0 for v in peer_avg]
    avg_vals += avg_vals[:1]
    ax.plot(angles, avg_vals, color="#ff7f0e", linewidth=2, linestyle="--")

    title = f"{company_id} — Peer Radar"
    plt.title(title, fontsize=12)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def draw_single_metric(company_id: str, comp_value: float, nifty_avg: float, out_path: str):
    # single-axis radar: create a triangular radar with company vs nifty
    labels = ["Composite"]
    N = 1
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    plt.xticks(angles[:-1], labels, fontsize=10)
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75], ["25", "50", "75"], color="grey", size=8)
    plt.ylim(0, 1)

    vals = [comp_value]
    vals += vals[:1]
    ax.plot(angles, vals, color="#1f77b4", linewidth=2)
    ax.fill(angles, vals, color="#1f77b4", alpha=0.25)

    avg_vals = [nifty_avg]
    avg_vals += avg_vals[:1]
    ax.plot(angles, avg_vals, color="#ff7f0e", linewidth=2, linestyle="--")

    plt.title(f"{company_id} — Composite vs Nifty", fontsize=12)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def generate_radar_charts(peer_excel_path: str = "data/peer_groups.xlsx", out_dir: str = "reports/radar_charts"):
    ensure_dir(out_dir)

    # load peer groups
    if os.path.exists(peer_excel_path):
        df_peers = pd.read_excel(peer_excel_path)
        if "company_id" not in df_peers.columns or "peer_group_name" not in df_peers.columns:
            raise ValueError("peer_groups.xlsx must contain 'company_id' and 'peer_group_name'")
    else:
        df_peers = pd.DataFrame(columns=["company_id", "peer_group_name"])

    # prepare screener data
    engine = ScreenerEngine()
    engine.prepare()
    df = engine.df.copy()

    # Merge peer group info
    if not df_peers.empty:
        df = df.merge(df_peers[["company_id", "peer_group_name"]], on="company_id", how="left")
    else:
        df["peer_group_name"] = pd.NA

    # compute Nifty 100 median composite for fallback
    nifty_median_composite = df["composite_quality_score"].median()

    # group by peer_group_name
    for pg_name, group in df.groupby("peer_group_name"):
        if pd.isna(pg_name):
            # Companies without peer group: handle below
            continue

        # compute percentiles for each axis within this peer group
        pr_df = pd.DataFrame(index=group.index)
        for label, col in AXES:
            if col not in group.columns:
                pr_df[label] = pd.NA
                continue
            values = pd.to_numeric(group[col], errors="coerce")
            pr = percent_rank_series(values)
            # invert D/E
            if label == "D/E":
                pr = pr.apply(lambda x: 1.0 - x if pd.notna(x) else pd.NA)
            pr_df[label] = pr

        # peer average per axis
        peer_avg = pr_df.mean(axis=0, skipna=True).tolist()

        # draw chart per company in group
        for idx, row in group.iterrows():
            company_id = row["company_id"]
            company_vals = pr_df.loc[idx].tolist()
            out_path = os.path.join(out_dir, f"{company_id}_radar.png")
            draw_radar(company_id, company_vals, peer_avg, [t[0] for t in AXES], out_path)

    # handle companies without peer group
    no_group = df[df["peer_group_name"].isna()]
    for idx, row in no_group.iterrows():
        company_id = row["company_id"]
        comp = row.get("composite_quality_score", None)
        # normalize composite to percentile vs entire dataset
        comp_pr = percent_rank_series(df["composite_quality_score"]).loc[idx]
        nifty_pr = percent_rank_series(df["composite_quality_score"]).mean()
        out_path = os.path.join(out_dir, f"{company_id}_radar.png")
        draw_single_metric(company_id, comp_pr if pd.notna(comp_pr) else 0.0, nifty_pr if pd.notna(nifty_pr) else 0.0, out_path)

    print("Radar charts generated in:", out_dir)


if __name__ == "__main__":
    generate_radar_charts()
