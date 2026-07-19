"""
Sectors Page
Analyze companies and performance by sector.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.utils.db import (
    get_sector_analysis_data
)


def main():
    st.title("🏭 Sector Performance")
    
    sector_df = get_sector_analysis_data()

    if sector_df.empty:
        st.error("No sector data available")
        return

    sector_list = sorted(sector_df["broad_sector"].dropna().unique())

    selected_sector = st.selectbox(
        "Select Sector",
        sector_list
    )

    filtered_df = sector_df[
        sector_df["broad_sector"] == selected_sector
    ]
    st.subheader("Sector Bubble Chart")

    fig = px.scatter(
        filtered_df,
        x="sales",
        y="return_on_equity_pct",
        size="market_cap_crore",
        color="sub_sector",
        hover_name="company_name",
        size_max=45,
        title=f"{selected_sector} Companies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


if __name__ == "__main__":
    main()
