from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


def test_free_cash_flow():
    assert free_cash_flow(500, -150) == 350


def test_cfo_quality_high():
    assert cfo_quality_score(1200, 1000) == "High Quality"


def test_cfo_quality_none():
    assert cfo_quality_score(100, 0) is None


def test_capex_intensity():
    value, label = capex_intensity(-50, 1000)

    assert value == 5.0
    assert label == "Moderate"


def test_fcf_conversion():
    assert fcf_conversion_rate(350, 500) == 70.0


def test_fcf_conversion_none():
    assert fcf_conversion_rate(100, 0) is None


def test_capital_allocation():
    _, _, _, label = capital_allocation_pattern(
        500,
        -100,
        -50,
        1.2,
    )

    assert label == "Shareholder Returns"
