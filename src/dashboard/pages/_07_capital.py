"""
Capital Allocation Page
Portfolio recommendations and capital allocation analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.utils.db import (
    get_companies,
    get_sector_analysis_data
)


def main():
    st.title("💰 Capital Allocation")
    
    companies = get_sector_analysis_data()

    if companies.empty:
        st.error("No capital allocation data found.")
        return
    
    st.subheader("Capital Allocation Map")

    companies["Allocation Pattern"] = companies["return_on_equity_pct"].apply(
        lambda x: "High Return" if pd.notnull(x) and x >= 20 else "Standard Return"
    ) 

    fig = px.treemap(
        companies,
        path=["Allocation Pattern", "company_name"],
        values="market_cap_crore",
        color="broad_sector",
        title="Capital Allocation Treemap"
    )

    st.plotly_chart(fig, use_container_width=True)

    selected_pattern = st.selectbox(
        "Choose Allocation Pattern",
        companies["Allocation Pattern"].unique()
    )

    filtered = companies[
        companies["Allocation Pattern"] == selected_pattern
    ]

    st.markdown(f"### {selected_pattern} Companies")

    st.dataframe(
        filtered[
            [
                "company_name",
                "broad_sector",
                "market_cap_crore",
                "return_on_equity_pct"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()
