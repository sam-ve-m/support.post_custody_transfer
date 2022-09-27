from unittest.mock import MagicMock, patch, call

from src.domain.builders.snapshot import HTMLSnapshotBuilder
from src.domain.models.tables.blocked_assets.model import BlockedAssets
from src.domain.models.tables.onboarding.model import Onboarding
from src.domain.models.tables.pid.model import PID
from src.domain.models.tables.user_blocks.model import UserBlocks
from src.domain.models.tables.vai_na_cola.model import VaiNaColaReport
from src.domain.models.tables.wallet.model import Wallet
from src.domain.models.tables.warranty.model import Warranty
from src.domain.models.tables.warranty_assets.model import WarrantyAssets
import pytest

fake_snapshot = MagicMock()
dummy_pid = "pid"
dummy_onboarding = "onboarding"
dummy_wallet_table = "wallet"
dummy_vai_na_cola = "vai na cola"
dummy_asset_table = "asset table"
dummy_blocks_table = "blocks table"
dummy_warranty_table = "warranty table"
dummy_warranty = "warranty"
fake_portfolio = MagicMock()
dummy_wallet_id = "Id"
dummy_columns = ["Dummy"]
dummy_rows = [["Wallet"], ["Wallet"]]
dummy_wallet = MagicMock(columns=dummy_columns, rows=dummy_rows)


@pytest.fixture
def fake_builder():
    return HTMLSnapshotBuilder(fake_snapshot)


@patch.object(WarrantyAssets, "build", return_value=dummy_warranty_table)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_list", return_value=dummy_warranty_table)
def test_warranty_assets_table(mocked_table_builder, mocked_get_snapshot, fake_builder):
    response = fake_builder.warranty_assets_table()
    mocked_get_snapshot.assert_called_once_with(fake_snapshot)
    assert dummy_warranty_table in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_warranty_table,
                                                 table_name="Ativos Em Garantia",
                                                 color="darkblue")
    assert response == fake_builder


@patch.object(VaiNaColaReport, "build", return_value=dummy_vai_na_cola)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_list", return_value=dummy_vai_na_cola)
def test_vai_na_cola_table(mocked_table_builder, mocked_get_snapshot, fake_builder):
    response = fake_builder.vai_na_cola_table()
    mocked_get_snapshot.assert_called_once_with(fake_snapshot)
    assert dummy_vai_na_cola in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_vai_na_cola,
                                                 table_name="Vai na Cola",
                                                 color="darkgreen")
    assert response == fake_builder


@patch.object(PID, "build", return_value=dummy_pid)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_dict", return_value=dummy_pid)
def test_pid_table(mocked_table_builder, mocked_get_snapshot, fake_builder):
    response = fake_builder.pid_table()
    mocked_get_snapshot.assert_called_once_with(fake_snapshot)
    assert dummy_pid in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_pid,
                                                 table_name="PID",
                                                 color="black")
    assert response == fake_builder


@patch.object(Onboarding, "build", return_value=dummy_onboarding)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_list", return_value=dummy_onboarding)
def test_onboarding_table(mocked_table_builder, mocked_get_snapshot, fake_builder):
    response = fake_builder.onboarding_table()
    mocked_get_snapshot.assert_called_once_with(fake_snapshot)
    assert dummy_onboarding in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_onboarding,
                                                 table_name="Onboarding",
                                                 color="black")
    assert response == fake_builder


@patch.object(Wallet, "build", return_value=dummy_wallet)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_list", return_value=dummy_wallet_table)
def test_wallet_table(mocked_table_builder, mocked_get_wallet, fake_builder):
    response = fake_builder.wallet_table()
    mocked_get_wallet.assert_called_once_with(fake_snapshot)
    assert dummy_wallet_table in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_wallet,
                                                 table_name="Carteira",
                                                 color="purple")
    assert response == fake_builder


@patch.object(BlockedAssets, "build", return_value=dummy_asset_table)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_list", return_value=dummy_asset_table)
def test_blocked_assets_table(mocked_table_builder, mocked_get_snapshot, fake_builder):
    response = fake_builder.blocked_assets_table()
    mocked_get_snapshot.assert_called_once_with(fake_snapshot)
    assert dummy_asset_table in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_asset_table,
                                                 table_name="Ativos Bloqueados",
                                                 color="darkred")
    assert response == fake_builder


@patch.object(UserBlocks, "build", return_value=dummy_blocks_table)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_dict", return_value=dummy_blocks_table)
def test_user_blocks_table(mocked_table_builder, mocked_get_snapshot, fake_builder):
    response = fake_builder.user_blocks_table()
    mocked_get_snapshot.assert_called_once_with(fake_snapshot)
    assert dummy_blocks_table in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_blocks_table,
                                                 table_name="Bloqueio",
                                                 color="darkred")
    assert response == fake_builder


@patch.object(Warranty, "build", return_value=dummy_warranty)
@patch.object(HTMLSnapshotBuilder, "_create_table_from_dict", return_value=dummy_warranty)
def test_warranty_table(mocked_table_builder, mocked_get_snapshot, fake_builder):
    response = fake_builder.warranty_table()
    mocked_get_snapshot.assert_called_once_with(fake_snapshot)
    assert dummy_warranty in fake_builder.build()
    mocked_table_builder.assert_called_once_with(dummy_warranty,
                                                 table_name="Garantia",
                                                 color="darkblue")
    assert response == fake_builder
