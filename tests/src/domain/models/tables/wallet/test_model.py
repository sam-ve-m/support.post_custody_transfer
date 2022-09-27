from unittest.mock import MagicMock

from src.domain.models.tables.wallet.model import Wallet

dummy_wallet_id = "159951"
dummy_wallet_id_none = None
dummy_assets = [MagicMock(
    ticker='PETR4',
    mean_price=15.45,
    current_quantity=400,
    initial_quantity=150,
    spent_value=618,
    current_value=16,
)]
dummy_assets_empty = [MagicMock(
    ticker=None,
    mean_price=None,
    current_quantity=None,
    initial_quantity=None,
    spent_value=None,
    current_value=None,
)]
wallet_names = "Brazuca", "Gringa", "Vai na Cola BR"
expected_snapshot = [
    ['159951', wallet_name, 'PETR4', 15.45, 400, 150, 618, 16]
    for wallet_name in wallet_names
]
expected_example_snapshot = [
    ['159951', wallet_name, 'Exemplo', 'Exemplo', 'Exemplo', 'Exemplo', 'Exemplo', 'Exemplo']
    for wallet_name in wallet_names
]
dummy_wallet_name = "Brazuca"


def test_snapshot():
    setattr(Wallet, "wallet_name", dummy_wallet_name)
    snapshot = Wallet.build(MagicMock(portfolio=MagicMock(
        wallet_br=dummy_assets,
        wallet_id_br=MagicMock(bovespa_account=dummy_wallet_id),
        wallet_us=dummy_assets,
        wallet_id_us=MagicMock(dw_account=dummy_wallet_id),
        wallets_vnc_br={dummy_wallet_id: dummy_assets},
    )))
    assert snapshot.rows == expected_snapshot


def test_snapshot_example():
    setattr(Wallet, "wallet_name", dummy_wallet_name)
    snapshot = Wallet.build(MagicMock(portfolio=MagicMock(
        wallet_br=dummy_assets_empty,
        wallet_id_br=MagicMock(bovespa_account=dummy_wallet_id),
        wallet_us=dummy_assets_empty,
        wallet_id_us=MagicMock(dw_account=dummy_wallet_id),
        wallets_vnc_br={dummy_wallet_id: dummy_assets_empty},
    )))
    assert snapshot.rows == expected_example_snapshot
