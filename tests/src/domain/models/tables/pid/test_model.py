from unittest.mock import MagicMock

import pytest

from src.domain.models.tables.pid.model import PID


dummy_complete_user_data = MagicMock(
    email=True,
    cel_phone=True,
    identifier_document=MagicMock(cpf=True, document_data=MagicMock(number=True)),
    birth_date=True,
    portfolios=MagicMock(vnc=MagicMock(br=True)),
    mother_name=True,
    address=MagicMock(zip_code=True),
)

dummy_missing_user_data = MagicMock(
    email=None,
    cel_phone=None,
    identifier_document=MagicMock(cpf=None, document_data=MagicMock(number=None)),
    birth_date=None,
    portfolios=MagicMock(vnc=MagicMock(br=None)),
    mother_name=None,
    address=MagicMock(zip_code=None),
)


def test_set_email_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data, "email", dummy_missing_user_data.email)
    with pytest.raises(ValueError):
        PID.build(MagicMock(user=dummy_complete_user_data))


def test_set_telefone_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data, "cel_phone", dummy_missing_user_data.cel_phone)
    snapshot = PID.build(MagicMock(user=dummy_complete_user_data))
    assert snapshot.get("Telefone") == PID.NOT_FOUND_MESSAGE


def test_set_cpf_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data.identifier_document, "cpf", dummy_missing_user_data.identifier_document.cpf)
    with pytest.raises(ValueError):
        PID.build(MagicMock(user=dummy_complete_user_data))


def test_set_data_nascimento_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data, "birth_date", dummy_missing_user_data.birth_date)
    snapshot = PID.build(MagicMock(user=dummy_complete_user_data))
    assert snapshot.get("Data Nascimento") == PID.NOT_FOUND_MESSAGE


def test_set_possui_vai_na_cola_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data, "portfolios", dummy_missing_user_data.portfolios)
    snapshot = PID.build(MagicMock(user=dummy_complete_user_data))
    assert snapshot.get("Possui Vai na Cola?") is False


def test_set_rg_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data.identifier_document, "document_data", dummy_missing_user_data.identifier_document.document_data)
    snapshot = PID.build(MagicMock(user=dummy_complete_user_data))
    assert snapshot.get("RG") == PID.NOT_FOUND_MESSAGE


def test_set_nome_da_mae_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data, "mother_name", dummy_missing_user_data.mother_name)
    snapshot = PID.build(MagicMock(user=dummy_complete_user_data))
    assert snapshot.get("Nome da Mãe") == PID.NOT_FOUND_MESSAGE


def test_set_cep_not_in_snapshot(monkeypatch):
    monkeypatch.setattr(dummy_complete_user_data, "address", dummy_missing_user_data.address)
    snapshot = PID.build(MagicMock(user=dummy_complete_user_data))
    assert snapshot.get("CEP") == PID.NOT_FOUND_MESSAGE
