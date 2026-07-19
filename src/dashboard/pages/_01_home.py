"""
Home Page - Dashboard Overview with KPIs and Charts
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.utils.db import (
    get_home_screen_kpis, get_sector_breakdown, get_companies,
    get_financial_ratios_full, get_market_cap_data
)


def main():
    st.markdown('<div style="color: #1f77b4; font-size: 2.5rem; font-weight: bold;">Nifty 100 Analytics Dashboard</div>', 
                unsafe_allow_html=True)
    
    # Year selector in sidebar
    st.sidebar.markdown("### Dashboard Settings")
    selected_year = st.sidebar.selectbox(
        "Select Year:",
        options=list(range(2024, 2018, -1)),
        index=0,
        key="home_year"
    )
    
    # Get KPIs
    kpis = get_home_screen_kpis(year=selected_year) if selected_year else get_home_screen_kpis()
    
    # Display KPI tiles
    st.markdown("### Key Performance Indicators")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    def metric_card(col, label, value, unit=""):
        with col:
            st.metric(
                label=label,
                value=f"{value}{unit}",
                delta=None
            )
    
    metric_card(col1, "Avg ROE", kpis['avg_roe'], "%")
    metric_card(col2, "Median P/E", kpis['median_pe'], "x")
    metric_card(col3, "Median D/E", kpis['median_de'], "x")
    metric_card(col4, "Total Companies", kpis['total_companies'], "")
    metric_card(col5, "Median Revenue CAGR", kpis['median_revenue_cagr'], "%")
    metric_card(col6, "Debt-Free Cos", kpis['debt_free_count'], "")
    
    st.markdown("---")
    
    # Sector breakdown and top companies
    col_chart, col_table = st.columns([1.5, 1])
    
    with col_chart:
        st.markdown("### Sector Breakdown")
        sectors = get_sector_breakdown()
        
        if not sectors.empty:
            fig = go.Figure(data=[go.Pie(
                labels=sectors['broad_sector'],
                values=sectors['count'],
                hole=0.3,
                marker=dict(line=dict(color='white', width=2))
            )])
            fig.update_layout(
                height=400,
                showlegend=True,
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown("---")
    st.info("💡 Use the year selector in the sidebar to update all metrics to a specific year.")


if __name__ == "__main__":
    main()

