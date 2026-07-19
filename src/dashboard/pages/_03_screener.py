"""
Financial Screener Page
Filter and screen companies by financial criteria.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.utils.db import get_screener_data


def main():
    st.title("🔍 Financial Screener")
    
    # Get all screener data
    screener_df = get_screener_data()
    
    if screener_df.empty:
        st.error("No screening data available")
        return
    
    # Sidebar controls
    st.sidebar.markdown("### Screening Filters")
    
    # Create sliders with ranges
    filters = {}
    filters['roe_min'] = st.sidebar.slider("ROE % (Min)", 0.0, 50.0, 5.0, 1.0)

    filters['de_max'] = st.sidebar.slider("D/E (Max)", 0.0, 5.0, 5.0, 0.1)

    filters['fcf_min'] = st.sidebar.slider("FCF Cr (Min)", 0.0, 1000.0, 0.0, 50.0)

    filters['revenue_cagr_min'] = st.sidebar.slider("Revenue CAGR % (Min)", 0.0, 50.0, 0.0, 1.0)

    filters['pat_cagr_min'] = st.sidebar.slider("PAT CAGR % (Min)", 0.0, 50.0, 0.0, 1.0)

    filters['opm_min'] = st.sidebar.slider("OPM % (Min)", 0.0, 50.0, 0.0, 1.0)

    filters['pe_max'] = st.sidebar.slider("P/E (Max)", 5.0, 100.0, 100.0, 1.0)

    filters['pb_max'] = st.sidebar.slider("P/B (Max)", 1.0, 20.0, 20.0, 0.1)

    filters['div_yield_min'] = st.sidebar.slider("Div Yield % (Min)", 0.0, 10.0, 0.0, 0.1)

    filters['icr_min'] = st.sidebar.slider("ICR (Min)", 0.0, 20.0, 0.0, 0.5)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Preset Filters:**")
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("Quality", use_container_width=True):
            filters.update({
                "roe_min": 20.0,
                "de_max": 1.0,
                "fcf_min": 100.0,
                "revenue_cagr_min": 15.0,
                "pat_cagr_min": 15.0,
                "opm_min": 15.0,
                "pe_max": 50.0,
                "pb_max": 10.0,
                "div_yield_min": 0.0,
                "icr_min": 3.0,
          })
    with col2:
        if st.button("Value", use_container_width=True):
            st.session_state.preset = 'value'
    with col3:
        if st.button("Growth", use_container_width=True):
            st.session_state.preset = 'growth'
    
    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("Dividend", use_container_width=True):
            st.session_state.preset = 'dividend'
    with col2:
        if st.button("Debt-Free", use_container_width=True):
            st.session_state.preset = 'debt_free'
    with col3:
        if st.button("Turnaround", use_container_width=True):
            st.session_state.preset = 'turnaround'
    
    # Apply filters
    filtered_df = screener_df.copy()
    numeric_columns = [
        "roe",
        "de",
        "fcf",
        "revenue_cagr",
        "pat_cagr",
        "opm",
        "pe_ratio",
        "pb_ratio",
        "div_yield",
        "icr",
    ]

    for col in numeric_columns:
        if col in filtered_df.columns:
            filtered_df[col] = pd.to_numeric(
                filtered_df[col],
                errors="coerce"
            )   
    
    for col_name, column_key, operator in [
        ('roe', 'roe_min', '>='),
        ('de', 'de_max', '<='),
        ('fcf', 'fcf_min', '>='),
        ('revenue_cagr', 'revenue_cagr_min', '>='),
        ('pat_cagr', 'pat_cagr_min', '>='),
        ('opm', 'opm_min', '>='),
        ('pe_ratio', 'pe_max', '<='),
        ('pb_ratio', 'pb_max', '<='),
        ('div_yield', 'div_yield_min', '>='),
        ('icr', 'icr_min', '>='),
    ]:
        if column_key in filters and col_name in filtered_df.columns:
            if operator == '>=':
                filtered_df = filtered_df[filtered_df[col_name] >= filters[column_key]]
            elif operator == '<=':
                filtered_df = filtered_df[filtered_df[col_name] <= filters[column_key]]
    
    st.markdown("### Screening Results")
    st.markdown(f"**{len(filtered_df)} companies match your filters**")
    
    if not filtered_df.empty:
        display_columns = ['id', 'company_name', 'broad_sector', 'composite_score', 'roe', 'de', 'fcf', 'revenue_cagr', 'opm', 'pe_ratio', 'div_yield']
        available_cols = [c for c in display_columns if c in filtered_df.columns]
        display_df = filtered_df[available_cols].copy()
        display_df.columns = ['Ticker', 'Company', 'Sector', 'Score', 'ROE%', 'D/E', 'FCF Cr', 'Rev CAGR%', 'OPM%', 'P/E', 'Div Yield%']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv_data = filtered_df.to_csv(index=False)
        st.download_button("📥 Download CSV", data=csv_data, file_name="screened_companies.csv", mime="text/csv")
    else:
        st.warning("No companies match the selected criteria.")


if __name__ == "__main__":
    main()
