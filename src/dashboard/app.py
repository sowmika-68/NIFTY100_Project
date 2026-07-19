"""
Nifty 100 Analytics Dashboard - Main Entry Point
A comprehensive Streamlit application for analyzing Nifty 100 companies.
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure Streamlit page settings
st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Nifty 100 Analytics Dashboard\nBuilt with Streamlit",
    }
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application entry point with sidebar navigation."""
    
    # Sidebar title
    st.sidebar.markdown("## 📊 Navigation")
    
    # Navigation menu
    page = st.sidebar.radio(
        "Select a page:",
        [
            "🏠 Home",
            "👤 Company Profile",
            "🔍 Screener",
            "📈 Peers",
            "📊 Trends",
            "🏭 Sectors",
            "💰 Capital Allocation",
            "📋 Reports"
        ],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This dashboard provides comprehensive analytics for Nifty 100 companies, including "
        "financial ratios, valuation metrics, peer comparison, and sector analysis."
    )
    
    # Route to appropriate page
    if page == "🏠 Home":
        show_home()
    elif page == "👤 Company Profile":
        show_profile()
    elif page == "🔍 Screener":
        show_screener()
    elif page == "📈 Peers":
        show_peers()
    elif page == "📊 Trends":
        show_trends()
    elif page == "🏭 Sectors":
        show_sectors()
    elif page == "💰 Capital Allocation":
        show_capital_allocation()
    elif page == "📋 Reports":
        show_reports()


def show_home():
    """Home page - Dashboard overview."""
    from dashboard.pages import _01_home as page
    page.main()


def show_profile():
    """Company Profile page."""
    from dashboard.pages import _02_profile as page
    page.main()


def show_screener():
    """Screener page."""
    from dashboard.pages import _03_screener as page
    page.main()


def show_peers():
    """Peers comparison page."""
    from dashboard.pages import _04_peers as page
    page.main()


def show_trends():
    """Trends analysis page."""
    from dashboard.pages import _05_trends as page
    page.main()


def show_sectors():
    """Sectors analysis page."""
    from dashboard.pages import _06_sectors as page
    page.main()


def show_capital_allocation():
    """Capital allocation page."""
    from dashboard.pages import _07_capital as page
    page.main()


def show_reports():
    """Reports page."""
    from dashboard.pages import _08_reports as page
    page.main()


if __name__ == "__main__":
    main()
