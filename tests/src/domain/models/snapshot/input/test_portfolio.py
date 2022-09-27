from unittest.mock import patch

from src.domain.models.snapshot.input.portfolio import PortfolioWalletBR, PortfolioWalletUS, Asset, \
    VaiNaColaWalletReport, Portfolio

dummy_value = "value"
stub_portfolio_br = {"bmf_account": dummy_value, "bovespa_account": dummy_value}
stub_portfolio_us = {"dw_account": dummy_value}
stub_asset = {
    "ticker": dummy_value,
    "mean_price": dummy_value,
    "spent_value": dummy_value,
    "current_value": dummy_value,
    "current_quantity": dummy_value,
    "initial_quantity": dummy_value,
}
stub_portfolio = {
    "warranty": [{dummy_value: dummy_value}],
    "wallet_us": [{dummy_value: dummy_value}],
    "wallet_br": [{dummy_value: dummy_value}],
    "wallet_id_br": {dummy_value: dummy_value},
    "wallet_id_us": {dummy_value: dummy_value},
    "wallets_vnc_br_report": [{dummy_value: dummy_value}],
    "wallets_vnc_br": {dummy_value: [{dummy_value: dummy_value}]},
}
stub_portfolio_empty = {
    "wallet_us": [],
    "wallet_br": [],
    "wallet_id_br": {},
    "wallet_id_us": {},
    "wallets_vnc_br": {},
}


def test_instance_portfolio_br_with_content():
    portfolio_br = PortfolioWalletBR.build(**stub_portfolio_br)
    assert portfolio_br.bovespa_account == dummy_value
    assert portfolio_br.bmf_account == dummy_value


def test_instance_portfolio_br_empty():
    portfolio_br = PortfolioWalletBR.build()
    assert portfolio_br.bmf_account is None
    assert portfolio_br.bovespa_account is None


def test_instance_portfolio_us_with_content():
    portfolio_us = PortfolioWalletUS.build(**stub_portfolio_us)
    assert portfolio_us.dw_account == dummy_value


def test_instance_portfolio_us_empty():
    portfolio_us = PortfolioWalletUS.build()
    assert portfolio_us.dw_account is None


def test_instance_asset_with_content():
    asset = Asset.from_dict(stub_asset)
    assert asset.ticker == dummy_value
    assert asset.mean_price == dummy_value
    assert asset.spent_value == dummy_value
    assert asset.current_value == dummy_value
    assert asset.current_quantity == dummy_value
    assert asset.initial_quantity == dummy_value


def test_instance_asset_empty():
    asset = Asset.from_dict(None)
    assert asset.ticker is None
    assert asset.mean_price is None
    assert asset.spent_value is None
    assert asset.current_value is None
    assert asset.current_quantity is None
    assert asset.initial_quantity is None


@patch.object(Asset, "from_dict", side_effect=lambda x: x)
@patch.object(PortfolioWalletBR, "build", side_effect=lambda **x: x)
@patch.object(PortfolioWalletUS, "build", side_effect=lambda **x: x)
@patch.object(VaiNaColaWalletReport, "__init__", return_value=None)
def test_instance_portfolio_with_content(
    mocked_vai_na_cola_wallet_report,
    mocked_portfolio_wallet_us,
    mocked_portfolio_wallet_br,
    mocked_asset,
):
    portfolio = Portfolio.build(**stub_portfolio)
    assert portfolio.warranty == [{dummy_value: dummy_value}]
    assert portfolio.wallet_us == [{dummy_value: dummy_value}]
    assert portfolio.wallet_br == [{dummy_value: dummy_value}]
    assert portfolio.wallet_id_br == {dummy_value: dummy_value}
    assert portfolio.wallet_id_us == {dummy_value: dummy_value}
    assert portfolio.wallets_vnc_br == {dummy_value: [{}]}
    mocked_vai_na_cola_wallet_report.assert_called_once_with(**{dummy_value: dummy_value})


@patch.object(Asset, "from_dict", side_effect=lambda x: x)
@patch.object(PortfolioWalletBR, "build", side_effect=lambda **x: x)
@patch.object(PortfolioWalletUS, "build", side_effect=lambda **x: x)
@patch.object(VaiNaColaWalletReport, "__init__", return_value=None)
def test_instance_portfolio_empty(
    mocked_vai_na_cola_wallet_report,
    mocked_portfolio_wallet_us,
    mocked_portfolio_wallet_br,
    mocked_asset,
):
    portfolio = Portfolio.build(**stub_portfolio_empty)
    assert portfolio.warranty == []
    assert portfolio.wallet_us == []
    assert portfolio.wallet_br == []
    assert portfolio.wallet_id_br == {}
    assert portfolio.wallet_id_us == {}
    assert portfolio.wallets_vnc_br == {}
    assert portfolio.wallets_vnc_br_report == []
    mocked_vai_na_cola_wallet_report.assert_not_called()

