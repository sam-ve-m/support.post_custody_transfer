from unittest.mock import MagicMock

import pytest

from src.domain.models.tables.blocked_assets.model import BlockedAssets

dummy_blocked_assets = [MagicMock(
    ticker='Sem definição',
    mean_price='Sem definição',
    current_quantity='Sem definição',
)]*3
dummy_blocked_assets_empty = [MagicMock(
    ticker=None,
    mean_price=None,
    current_quantity=None,
)]*2


dummy_columns = ['Ativo', 'Preço Médio', 'Quantidade']
dummy_rows = [['Sem definição', 'Sem definição', 'Sem definição']]


def test_get_snapshot():
    snapshot = BlockedAssets.build(MagicMock(blocked_assets=dummy_blocked_assets))
    assert snapshot.columns == dummy_columns and snapshot.rows == dummy_rows*3


def test_get_snapshot_empty():
    snapshot = BlockedAssets.build(MagicMock(blocked_assets=dummy_blocked_assets_empty))
    assert snapshot.columns == dummy_columns and snapshot.rows == dummy_rows*2
