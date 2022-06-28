from unittest.mock import MagicMock, patch


# Jormungandr
from func.src.domain.snapshot.html.tables.blocked_assets import BlockedAssetsTableDTO
from func.src.domain.snapshot.html.tables.onboarding import OnboardingTableDTO
from func.src.domain.snapshot.html.tables.pid import PIDTableDTO
from func.src.domain.snapshot.html.tables.user_blocks import UserBlocksTableDTO
from func.src.domain.snapshot.html.tables.vai_na_cola import VaiNaColaTableDTO
from func.src.domain.snapshot.html.tables.wallet import WalletTableDTO
from func.src.domain.snapshot.html.tables.warranty import WarrantyTableDTO
from func.src.domain.snapshot.html.tables.warranty_assets import WarrantyAssetsTableDTO
from func.src.services.snapshot import SnapshotUserDataService

dummy_jwt = "sd8a1f95dba9e85rza16s5d1vads"
dummy_filled_table = "<table></table>"
dummy_empty_table = ""
dummy_full_table = (
    '<table></table><table></table>'
    '</br></br>'
    '<table></table>'
    '</br></br>'
    '<table></table>'
    '</br></br>'
    '<table></table><table></table>'
    '</br></br>'
    '<table></table><table></table>'
)
dummy_partial_table = (
    '<table></table>'
    '</br></br>'
    '<table></table>'
    '</br></br>'
    '<table></table>'
    '</br></br>'
    '<table></table><table></table>'
)


@patch.object(BlockedAssetsTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(OnboardingTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(PIDTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(UserBlocksTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(VaiNaColaTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(WalletTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(WarrantyTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(WarrantyAssetsTableDTO, "create_table", return_value=dummy_filled_table)
def test_get_snapshot(
        mocked_warranty_assets_table_DTO,
        mocked_warranty_table_DTO,
        mocked_wallet_table_DTO,
        mocked_user_blocks_table_DTO,
        mocked_vai_na_cola_table_DTO,
        mocked_pid_table_DTO,
        mocked_onboarding_table_DTO,
        mocked_blocked_assets_table_DTO,
        monkeypatch,
):
    monkeypatch.setattr(SnapshotUserDataService, "snapshot_repository", MagicMock())
    response = SnapshotUserDataService.get_snapshot(dummy_jwt)
    assert response == dummy_full_table


@patch.object(BlockedAssetsTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(OnboardingTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(PIDTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(UserBlocksTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(VaiNaColaTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(WalletTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(WarrantyTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(WarrantyAssetsTableDTO, "create_table", return_value=dummy_empty_table)
def test_snapshot_empty_user_data(
        mocked_warranty_assets_table_DTO,
        mocked_warranty_table_DTO,
        mocked_wallet_table_DTO,
        mocked_user_blocks_table_DTO,
        mocked_vai_na_cola_table_DTO,
        mocked_pid_table_DTO,
        mocked_onboarding_table_DTO,
        mocked_blocked_assets_table_DTO,
        monkeypatch,
):
    monkeypatch.setattr(SnapshotUserDataService, "snapshot_repository", MagicMock())
    response = SnapshotUserDataService.get_snapshot(dummy_jwt)
    assert response == dummy_empty_table


@patch.object(BlockedAssetsTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(OnboardingTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(PIDTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(UserBlocksTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(VaiNaColaTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(WalletTableDTO, "create_table", return_value=dummy_empty_table)
@patch.object(WarrantyTableDTO, "create_table", return_value=dummy_filled_table)
@patch.object(WarrantyAssetsTableDTO, "create_table", return_value=dummy_filled_table)
def test_snapshot_partial_user_data(
        mocked_warranty_assets_table_DTO,
        mocked_warranty_table_DTO,
        mocked_wallet_table_DTO,
        mocked_user_blocks_table_DTO,
        mocked_vai_na_cola_table_DTO,
        mocked_pid_table_DTO,
        mocked_onboarding_table_DTO,
        mocked_blocked_assets_table_DTO,
        monkeypatch,
):
    monkeypatch.setattr(SnapshotUserDataService, "snapshot_repository", MagicMock())
    response = SnapshotUserDataService.get_snapshot(dummy_jwt)
    assert response == dummy_partial_table
