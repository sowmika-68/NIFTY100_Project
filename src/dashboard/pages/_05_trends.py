"""
Trends Analysis Page
Analyze historical trends for selected company.
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.utils.db import get_all_tickers, get_pl, get_cf


def main():
    st.title("📊 Trend Analysis")
    
    tickers = get_all_tickers()
    
    if not tickers:
        st.error("No companies found in database")
        return
    
    selected_ticker = st.selectbox(
        "Select Company:",
        tickers,
        key="trend_company"
    )
    
    if selected_ticker:
          metric_options = [
        "Revenue",
        "Net Profit",
        "Operating Cash Flow"
    ]

          selected_metrics = st.multiselect(
        "Select up to 3 Metrics",
        metric_options,
        default=["Revenue"],
        max_selections=3
    )

    # Get historical data
    pl = get_pl(selected_ticker)
    cf = get_cf(selected_ticker)

    fig = go.Figure()

    if "Revenue" in selected_metrics and not pl.empty:
        temp = pl.sort_values("year").tail(10)
        fig.add_trace(
            go.Scatter(
                x=temp["year"],
                y=temp["sales"],
                mode="lines+markers",
                name="Revenue"
            )
        )

    if "Net Profit" in selected_metrics and not pl.empty:
        temp = pl.sort_values("year").tail(10)
        fig.add_trace(
            go.Scatter(
                x=temp["year"],
                y=temp["net_profit"],
                mode="lines+markers",
                name="Net Profit"
            )
        )

    if "Operating Cash Flow" in selected_metrics and not cf.empty:
        temp = cf.sort_values("year").tail(10)
        fig.add_trace(
            go.Scatter(
                x=temp["year"],
                y=temp["operating_activity"],
                mode="lines+markers",
                name="Operating Cash Flow"
            )
        )

    fig.update_layout(
        title=f"{selected_ticker} - 10 Year Financial Trends",
        xaxis_title="Year",
        yaxis_title="Value",
        template="plotly_white",
        height=550,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    if len(fig.data) == 0:
        st.warning("No financial data available for the selected company.")
        return
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
