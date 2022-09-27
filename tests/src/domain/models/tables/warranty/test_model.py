from unittest.mock import MagicMock

from src.domain.models.tables.warranty.model import Warranty

dummy_user_empty = MagicMock(available=None)
dummy_user = MagicMock(available=15154848)
expected_snapshot = {'Disponível em Garantia': 15154848}
expected_snapshot_empty = {'Disponível em Garantia': "Sem definição"}


def test_get_snapshot():
    snapshot = Warranty.build(MagicMock(warranty=dummy_user))
    assert snapshot == expected_snapshot


def test_get_snapshot_empty():
    snapshot = Warranty.build(MagicMock(warranty=dummy_user_empty))
    assert snapshot == expected_snapshot_empty
