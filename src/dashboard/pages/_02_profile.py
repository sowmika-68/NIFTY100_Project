"""
Company Profile Page - Detailed financials, ratios, and analysis
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
    get_all_tickers, get_company_details, get_company_search_suggestions,
    get_financial_ratios_full, get_pl, get_market_cap_data, get_proscons
)


def main():
    st.title("👤 Company Profile")
    
    # Search section
    st.markdown("### Search Company")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_text = st.text_input(
            "Search by Company Name or Ticker:",
            placeholder="e.g., TCS or Tata Consultancy"
        )
    
    selected_company = None
    ticker = None
    
    if search_text:
        suggestions = get_company_search_suggestions(search_text)
        if suggestions:
            selected_company = st.selectbox(
                "Select Company:",
                suggestions,
                key="company_search"
            )
            ticker = selected_company.split(" - ")[0] if selected_company else None
    
    if not ticker:
        st.info("💡 Start typing a company name or ticker to search")
        return
    
    # Get company details
    try:
        company_info = get_company_details(ticker)
        
        if not company_info:
            st.error(f"🔍 Ticker not found — please try another")
            return
        
        # Company Card
        st.markdown("### Company Card")
        
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            st.markdown(f"**Company:** {company_info.get('company_name', 'N/A')}")
            st.markdown(f"**Sector:** {company_info.get('broad_sector', 'N/A')}")
        
        with col2:
            st.markdown(f"**Sub-Sector:** {company_info.get('sub_sector', 'N/A')}")
            st.markdown(f"**NSE Ticker:** {ticker}")
        
        with col3:
            st.markdown(f"**Book Value:** ₹{company_info.get('book_value', 'N/A')}")
            st.markdown(f"**About:** {str(company_info.get('about_company', 'N/A'))[:100]}...")
        
        st.markdown("---")
        
        # Get latest financial data
        latest_ratios = get_financial_ratios_full(ticker)
        latest_pl = get_pl(ticker)
        
        if not latest_ratios.empty:
            latest_year = latest_ratios.iloc[0]
            
            # KPI Tiles
            st.markdown("### Key Financial Metrics")
            
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            
            metrics = {
                col1: ("ROE %", latest_year.get('return_on_equity_pct', 0)),
                col2: ("ROCE %", 0),
                col3: ("NPM %", latest_year.get('net_profit_margin_pct', 0)),
                col4: ("D/E", latest_year.get('debt_to_equity', 0)),
                col5: ("Rev CAGR %", 0),  # From analysis table
                col6: ("FCF Cr", latest_year.get('free_cash_flow_cr', 0)),
            }
            
            for col, (label, value) in metrics.items():
                with col:
                    st.metric(label, f"{value:.2f}" if isinstance(value, (int, float)) else value)
            
            st.markdown("---")
            
            # Charts
            st.markdown("### Financial Trends")
            
            col_chart1, col_chart2 = st.columns(2)
            
            # Revenue and Net Profit Chart
            with col_chart1:
                st.markdown("#### Revenue & Net Profit (10Y)")
                
                if not latest_pl.empty:
                    pl_data = latest_pl.tail(10).sort_values('year')
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=pl_data['year'],
                        y=pl_data['sales'],
                        name='Revenue',
                        marker_color='#1f77b4'
                    ))
                    fig.add_trace(go.Bar(
                        x=pl_data['year'],
                        y=pl_data['net_profit'],
                        name='Net Profit',
                        marker_color='#ff7f0e'
                    ))
                    
                    fig.update_layout(
                        height=350,
                        barmode='group',
                        template='plotly_white',
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # ROE and ROCE Line Chart
            with col_chart2:
                st.markdown("#### ROE & ROCE Trends (10Y)")
                
                if not latest_ratios.empty:
                    ratios_data = latest_ratios.tail(10).sort_values('year')
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=ratios_data['year'],
                        y=ratios_data['return_on_equity_pct'],
                        name='ROE %',
                        mode='lines+markers',
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=6)
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=ratios_data['year'],
                        y=ratios_data['return_on_capital_employed_pct'],
                        name='ROCE %',
                        mode='lines+markers',
                        line=dict(color='green', width=2),
                        marker=dict(size=6)
                    ))

                    fig.update_layout(
                        height=350,
                        template='plotly_white',
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Pros and Cons
            st.markdown("### Pros & Cons")
            
            proscons = get_proscons(ticker)
            
            col_pros, col_cons = st.columns(2)
            
            with col_pros:
                st.markdown("#### ✅ Strengths")
                if not proscons.empty and proscons.iloc[0].get('pros'):
                    pros_list = str(proscons.iloc[0]['pros']).split(',')
                    for pro in pros_list[:5]:
                        st.write(f"✓ {pro.strip()}")
                else:
                    st.write("No data available")
            
            with col_cons:
                st.markdown("#### ❌ Challenges")
                if not proscons.empty and proscons.iloc[0].get('cons'):
                    cons_list = str(proscons.iloc[0]['cons']).split(',')
                    for con in cons_list[:5]:
                        st.write(f"✗ {con.strip()}")
                else:
                    st.write("No data available")
        else:
            st.info("No financial data available for this company")
    
    except KeyError:
        st.error("🔍 Ticker not found — please try another")


if __name__ == "__main__":
    main()
