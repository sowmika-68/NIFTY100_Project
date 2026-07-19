"""
Peers Comparison Page - Radar charts and KPI tables
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dashboard.utils.db import (
    get_all_tickers, get_peer_groups_list, get_peer_group_members,
    get_financial_ratios_full
)


def main():
    st.title("📈 Peer Comparison")
    
    peer_groups = get_peer_groups_list()
    
    if not peer_groups:
        st.error("No peer groups found")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_group = st.selectbox("Select Peer Group:", peer_groups)
    
    with col2:
        selected_company = st.selectbox("Select Company:", get_all_tickers())
    
    if selected_group:
        members = get_peer_group_members(selected_group)
        
        if members.empty:
            st.warning(f"No data for {selected_group}")
            return
        
        st.markdown(f"### {selected_group} Group")
        st.markdown(f"**Companies: {len(members)}**")
        
        col_chart, col_table = st.columns([1.3, 1])
        
        with col_chart:
            st.markdown("#### Radar Chart Comparison")
            if selected_company in members['company_id'].values:
                fig = create_radar_chart(members, selected_company)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"{selected_company} not in {selected_group}")
        
        with col_table:
            st.markdown("#### Group Metrics")
            display_df = members[['company_id', 'company_name', 'return_on_equity_pct', 'debt_to_equity', 'is_benchmark']].copy()
            display_df.columns = ['Ticker', 'Company', 'ROE%', 'D/E', 'Benchmark']
            st.dataframe(display_df, use_container_width=True, hide_index=True)


def create_radar_chart(members_df, benchmark_ticker):
    """Create radar chart for peer comparison"""
    
    metrics = ['return_on_equity_pct', 'debt_to_equity', 'net_profit_margin_pct', 'free_cash_flow_cr']
    metric_labels = ['ROE%', 'D/E', 'NPM%', 'FCF Cr']
    
    benchmark_row = members_df[members_df['company_id'] == benchmark_ticker].iloc[0]
    group_avg = members_df[metrics].mean()
    
    benchmark_vals = [benchmark_row.get(m, 0) or 0 for m in metrics]
    group_vals = [group_avg.get(m, 0) or 0 for m in metrics]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=benchmark_vals,
        theta=metric_labels,
        fill='toself',
        name=benchmark_ticker,
        line=dict(color='#1f77b4')
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=group_vals,
        theta=metric_labels,
        fill='toself',
        name='Group Average',
        line=dict(color='#ff7f0e')
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(max(benchmark_vals), max(group_vals)) * 1.2])),
        height=400,
        template='plotly_white'
    )
    
    return fig


if __name__ == "__main__":
    main()
