from unittest.mock import MagicMock

from src.domain.models.tables.vai_na_cola.model import VaiNaColaReport

no_vnc_wallets = []
expected_snapshot_empty = []


def test_model_instance_empty():
    snapshot = VaiNaColaReport.build(MagicMock(portfolio=MagicMock(wallets_vnc_br_report=no_vnc_wallets)))
    assert snapshot.rows == expected_snapshot_empty


dummy_id = "Id"
dummy_wallet = [MagicMock(id=dummy_id)]*3
expected_snapshot = [[
    dummy_id,
    'Pendente de Definição',
    'Pendente de Definição',
    'Pendente de Definição',
    'Pendente de Definição',
    'Pendente de Definição',
]]*3


def test_model_instance():
    snapshot = VaiNaColaReport.build(MagicMock(portfolio=MagicMock(wallets_vnc_br_report=dummy_wallet)))
    assert snapshot.rows == expected_snapshot
