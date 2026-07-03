from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning_flag,
    net_debt,
    asset_turnover,
    is_financial_company,
)


def test_net_profit_margin():
    assert net_profit_margin(100, 500) == 20.0


def test_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(150, 1000) == 15.0


def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(150, 0) is None


def test_opm_cross_check():
    value = operating_profit_margin(operating_profit=150, sales=1000, opm_percentage=25)

    assert value == 15.0


def test_return_on_equity():
    assert return_on_equity(net_profit=200, equity_capital=500, reserves=500) == 20.0


def test_negative_equity():
    assert return_on_equity(net_profit=100, equity_capital=-200, reserves=100) is None


def test_return_on_capital_employed():
    assert (
        round(
            return_on_capital_employed(
                ebit=150, equity_capital=500, reserves=500, borrowings=500
            ),
            2,
        )
        == 10.00
    )


def test_roce_zero_capital():
    assert (
        return_on_capital_employed(ebit=100, equity_capital=0, reserves=0, borrowings=0)
        is None
    )


def test_is_financial_company():
    assert is_financial_company("Financials") is True
    assert is_financial_company("IT") is False


def test_return_on_assets():
    assert return_on_assets(net_profit=100, total_assets=1000) == 10.0


def test_return_on_assets_zero_assets():
    assert return_on_assets(net_profit=100, total_assets=0) is None


def test_debt_to_equity_debt_free():
    assert debt_to_equity(0, 500, 500) == 0


def test_interest_coverage_ratio():
    assert interest_coverage_ratio(100, 20, 40) == 3.0


def test_interest_zero():
    assert interest_coverage_ratio(100, 20, 0) is None


def test_icr_label():
    assert icr_label(0) == "Debt Free"


def test_icr_warning_flag():
    assert icr_warning_flag(1.2) is True
    assert icr_warning_flag(3.5) is False


def test_net_debt():
    assert net_debt(500, 200) == 300


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0


def test_asset_turnover_zero_assets():
    assert asset_turnover(1000, 0) is None
