"""
Sprint 2 - Day 11

Cash Flow KPI Engine
"""

from typing import Optional


def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Calculate Free Cash Flow.

    If either value is missing,
    return None.
    """

    if operating_activity is None:
        return None

    if investing_activity is None:
        return None

    return operating_activity + investing_activity


def cfo_quality_score(cfo_total: float, pat_total: float):
    """
    Calculate CFO Quality Score.

    Ratio = CFO / PAT
    """

    if pat_total == 0:
        return None

    ratio = cfo_total / pat_total

    if ratio > 1:
        return "High Quality"

    if ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity: float, sales: float):
    """
    Calculate CapEx Intensity.
    """

    if sales == 0:
        return None

    value = (abs(investing_activity) / sales) * 100

    if value < 3:
        category = "Asset Light"

    elif value <= 8:
        category = "Moderate"

    else:
        category = "Capital Intensive"

    return round(value, 2), category


def fcf_conversion_rate(
    free_cash_flow: float, operating_profit: float
) -> Optional[float]:
    """
    Calculate FCF Conversion Rate.
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100


def capital_allocation_pattern(
    cfo: float, cfi: float, cff: float, cfo_pat_ratio: float = None
):
    """
    Classify capital allocation pattern based on
    CFO, CFI and CFF signs.
    """

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Unknown"

    return (cfo_sign, cfi_sign, cff_sign, label)
