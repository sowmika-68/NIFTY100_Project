# Quick script to fix the get_home_screen_kpis function

import re

def extract_percentage(val):
    """Extract percentage number from string like '10 Years: 11%'"""
    if pd.isna(val) or val is None:
        return None
    if isinstance(val, (int, float)):
        return float(val)
    try:
        # Try to extract number from string
        match = re.search(r'(\d+\.?\d*)', str(val))
        if match:
            return float(match.group(1))
    except:
        pass
    return None

# The fix would be in get_home_screen_kpis:
# After reading cagr_data:
# cagr_data['compounded_sales_growth'] = cagr_data['compounded_sales_growth'].apply(extract_percentage)
