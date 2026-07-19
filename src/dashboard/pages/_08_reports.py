"""
Reports Page
Generate and export custom reports.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.utils.db import (
    get_all_tickers,
    get_ratios,
    get_valuation_data,
    get_annual_reports
)

def main():

    st.title("📄 Annual Reports")

    tickers = get_all_tickers()

    company = st.selectbox(
        "Select Company",
        tickers
    )

    reports = get_annual_reports(company)

    if reports.empty:
        st.warning("No annual reports available.")
        return

    st.subheader("Available Reports")
    st.markdown("---")

    st.subheader("Valuation Summary")

    valuation_df = get_valuation_data()

    if not valuation_df.empty:

        st.dataframe(
            valuation_df,
            use_container_width=True,
            hide_index=True
        )

        csv = valuation_df.to_csv(index=False)

        st.download_button(
            "📥 Download Valuation Report",
            csv,
            file_name="valuation_summary.csv",
            mime="text/csv"
        ) 

    for _, row in reports.iterrows():

        year = row["Year"]
        url = row["Annual_Report"]

        col1, col2 = st.columns([1,3])

        with col1:
            st.write(year)

        with col2:

            if url and str(url).startswith("http"):

                st.markdown(
                    f"[📥 Open Annual Report]({url})"
                )

            else:

                st.error("Report unavailable")
    st.markdown("---")
    st.subheader("Latest Valuation Summary")

    valuation_df = get_valuation_data()

    if valuation_df.empty:
        st.warning("No valuation data available.")
    else:
        st.dataframe(
            valuation_df,
            use_container_width=True,
            hide_index=True
        )

        csv = valuation_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Valuation Summary",
            data=csv,
            file_name="valuation_summary.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()