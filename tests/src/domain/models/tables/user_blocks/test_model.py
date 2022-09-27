from unittest.mock import MagicMock

from src.domain.models.tables.user_blocks.model import UserBlocks
import pytest


nothing_missing = MagicMock(
    block_type='block_type',
    description='description',
    date='date',
    lawsuit_number='lawsuit_number'
), {
    'Tipo de bloqueio': 'block_type',
    'Descrição': 'description',
    'Data e Hora': 'date',
    'Numero do Processo (Caso bloqueio judicial)': 'lawsuit_number'
}
all_missing = MagicMock(
    block_type=None,
    description=None,
    date=None,
    lawsuit_number=None,
), {
    'Tipo de bloqueio': 'Sem definição',
    'Descrição': 'Sem definição',
    'Data e Hora': 'Sem definição',
    'Numero do Processo (Caso bloqueio judicial)': 'Sem definição'
}


@pytest.mark.parametrize("dummy_user,expected_snapshot", [all_missing, nothing_missing])
def test_get_snapshot(dummy_user, expected_snapshot):
    snapshot = UserBlocks.build(MagicMock(blocks=dummy_user))
    assert expected_snapshot == snapshot
