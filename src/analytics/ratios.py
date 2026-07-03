"""
Financial Ratio Engine
Sprint 2 - Day 08

This module contains functions to calculate
profitability ratios.
"""

import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """
    Calculate Net Profit Margin.

    Formula:
    Net Profit / Sales × 100

    Returns:
        None if sales is zero.
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(
    operating_profit,
    sales,
    opm_percentage=None
):
    """
    Calculate Operating Profit Margin.

    Returns None if sales is 0 or any required value is missing.
    """

    if operating_profit is None:
        return None

    if sales is None:
        return None

    if sales == 0:
        return None

    calculated_opm = (operating_profit / sales) * 100

    if opm_percentage is not None:
        if abs(calculated_opm - opm_percentage) > 1:
            logger.warning(
                f"OPM mismatch | Calculated: {calculated_opm:.2f} | Source: {opm_percentage:.2f}"
            )

    return calculated_opm


def return_on_equity(
    net_profit: float, equity_capital: float, reserves: float
) -> Optional[float]:
    """
    Calculate Return on Equity (ROE).

    Formula:
        Net Profit / (Equity Capital + Reserves) × 100

    Returns:
        None if Equity Capital + Reserves <= 0.
    """

    total_equity = equity_capital + reserves

    if total_equity <= 0:
        return None

    return (net_profit / total_equity) * 100


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings
):
    """
    Calculate Return on Capital Employed (ROCE).

    Returns None if any required value is missing
    or capital employed is zero or negative.
    """

    if (
        ebit is None
        or equity_capital is None
        or reserves is None
        or borrowings is None
    ):
        return None

    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return (ebit / capital_employed) * 100


def is_financial_company(broad_sector: str) -> bool:
    """
    Check whether a company belongs to the Financials sector.
    """

    return broad_sector.strip().lower() == "financials"


def return_on_assets(net_profit: float, total_assets: float) -> Optional[float]:
    """
    Calculate Return on Assets (ROA).

    Formula:
        Net Profit / Total Assets × 100

    Returns:
        None if total assets are zero.
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100


def debt_to_equity(
    borrowings: float, equity_capital: float, reserves: float
) -> Optional[float]:
    """
    Calculate Debt-to-Equity Ratio.

    Formula:
        Borrowings / (Equity Capital + Reserves)

    Rules:
        - Return 0 if borrowings are zero.
        - Return None if equity is less than or equal to zero.
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return borrowings / equity


def high_leverage_flag(
    debt_to_equity_ratio: Optional[float], broad_sector: str
) -> bool:
    """
    Return True when D/E > 5
    except Financials sector.
    """

    if debt_to_equity_ratio is None:
        return False

    if broad_sector.lower() == "financials":
        return False

    return debt_to_equity_ratio > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Calculate Interest Coverage Ratio.

    Returns None if any required value is missing
    or interest is zero.
    """

    if operating_profit is None:
        return None

    if other_income is None:
        return None

    if interest is None:
        return None

    if interest == 0:
        return None

    return (operating_profit + other_income) / interest


def icr_warning_flag(icr: Optional[float]) -> bool:
    """
    Return True if Interest Coverage Ratio is below 1.5.
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings: float, investments: float) -> float:
    """
    Calculate Net Debt.

    Formula:
        Borrowings - Investments
    """

    return borrowings - investments


def asset_turnover(sales: float, total_assets: float) -> Optional[float]:
    """
    Calculate Asset Turnover Ratio.

    Formula:
        Sales / Total Assets

    Returns:
        None if total assets are zero.
    """

    if total_assets == 0:
        return None

    return sales / total_assets

def icr_label(interest: float):
    """
    Return label for Interest Coverage Ratio.

    If interest is zero, the company is considered debt free.
    """

    if interest == 0:
        return "Debt Free"

    return None
