from unittest.mock import MagicMock

from src.domain.models.tables.warranty_assets.model import WarrantyAssets

dummy_assets = [MagicMock(
    ticker="Com definição",
    current_value="Com definição",
    current_quantity="Com definição",
)]*2
dummy_assets_empty = [MagicMock(
    ticker=None,
    current_value=None,
    current_quantity=None,
)]*2
expected_assets = [["Com definição"]*3]*2
expected_assets_empty = [["Sem definição"]*3]*2


def test_snapshot_empty():
    snapshot = WarrantyAssets.build(MagicMock(portfolio=MagicMock(warranty=dummy_assets_empty)))
    assert snapshot.rows == expected_assets_empty


def test_snapshot():
    snapshot = WarrantyAssets.build(MagicMock(portfolio=MagicMock(warranty=dummy_assets)))
    assert snapshot.rows == expected_assets

