"""
Sprint 2 - Day 10

CAGR Engine
"""

from typing import Optional, Tuple

DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
TURNAROUND = "TURNAROUND"
BOTH_NEGATIVE = "BOTH_NEGATIVE"
ZERO_BASE = "ZERO_BASE"
INSUFFICIENT = "INSUFFICIENT"
NORMAL = "NORMAL"


def calculate_cagr(
    start_value: float, end_value: float, years: int
) -> Tuple[Optional[float], str]:
    """
    Calculate CAGR with edge case handling.
    """

    if years <= 0:
        return None, INSUFFICIENT

    if start_value == 0:
        return None, ZERO_BASE

    if start_value > 0 and end_value < 0:
        return None, DECLINE_TO_LOSS

    if start_value < 0 and end_value > 0:
        return None, TURNAROUND

    if start_value < 0 and end_value < 0:
        return None, BOTH_NEGATIVE

    cagr = (((end_value / start_value) ** (1 / years)) - 1) * 100

    return round(cagr, 2), NORMAL


def revenue_cagr(start_revenue: float, end_revenue: float, years: int):
    """
    Calculate Revenue CAGR.
    """

    return calculate_cagr(start_revenue, end_revenue, years)


def pat_cagr(start_pat: float, end_pat: float, years: int):
    """
    Calculate PAT CAGR.
    """

    return calculate_cagr(start_pat, end_pat, years)


def eps_cagr(start_eps: float, end_eps: float, years: int):
    """
    Calculate EPS CAGR.
    """

    return calculate_cagr(start_eps, end_eps, years)
