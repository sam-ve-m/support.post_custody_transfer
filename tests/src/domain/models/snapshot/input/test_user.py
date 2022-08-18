from unittest.mock import patch

from src.domain.models.snapshot.input.user import DocumentData, IdentifierDocument, VncPortfolio, UserPortfolios, \
    Address, SnapshotUser

dummy_value = "value"
stub_document_data = {"number": dummy_value}
stub_identifier_document = {"cpf": dummy_value, "document_data": dummy_value}
stub_vnc = {"br": dummy_value}
stub_portfolio = {"vnc": dummy_value}
stub_address = {"zip_code": dummy_value}
stub_user = {
    "email": dummy_value,
    "cel_phone": dummy_value,
    "birth_date": dummy_value,
    "mother_name": dummy_value,
    "address": {dummy_value: dummy_value},
    "portfolios": {dummy_value: dummy_value},
    "identifier_document": {dummy_value: dummy_value},
}
stub_user_empty = {
    "email": None,
    "birth_date": None,
    "mother_name": None,
}


def test_instance_document_data_with_content():
    document_data = DocumentData.from_dict(stub_document_data)
    assert document_data.number == dummy_value


def test_instance_document_data_empty():
    document_data = DocumentData.from_dict(None)
    assert document_data.number is None


@patch.object(DocumentData, "from_dict", side_effect=lambda x: x)
def test_instance_identifier_document_with_content(mocked_from_dict):
    identifier_document = IdentifierDocument.build(**stub_identifier_document)
    assert identifier_document.document_data == dummy_value
    assert identifier_document.cpf == dummy_value


@patch.object(DocumentData, "from_dict", side_effect=lambda x: x)
def test_instance_identifier_document_empty(mocked_from_dict):
    identifier_document = IdentifierDocument.build()
    assert identifier_document.document_data is None
    assert identifier_document.cpf is None


def test_instance_vnc_with_content():
    vnc = VncPortfolio.from_dict(stub_vnc)
    assert vnc.br == dummy_value


def test_instance_vnc_empty():
    vnc = VncPortfolio.from_dict(None)
    assert vnc.br is None


@patch.object(VncPortfolio, "from_dict", side_effect=lambda x: x)
def test_instance_portfolio_with_content(mocked_from_dict):
    portfolio = UserPortfolios.build(**stub_portfolio)
    assert portfolio.vnc == dummy_value


@patch.object(VncPortfolio, "from_dict", side_effect=lambda x: x)
def test_instance_portfolio_empty(mocked_from_dict):
    portfolio = UserPortfolios.build()
    assert portfolio.vnc is None


def test_instance_address_with_content():
    address = Address.build(**stub_address)
    assert address.zip_code == dummy_value


def test_instance_address_empty():
    address = Address.build()
    assert address.zip_code is None


@patch.object(Address, "build", side_effect=lambda **x: x)
@patch.object(UserPortfolios, "build", side_effect=lambda **x: x)
@patch.object(IdentifierDocument, "build", side_effect=lambda **x: x)
def test_instance_user_with_content(mocked_build_document, mocked_build_portfolio, mocked_build_address):
    user = SnapshotUser.build(**stub_user)
    assert user.email == dummy_value
    assert user.cel_phone == dummy_value
    assert user.birth_date == dummy_value
    assert user.mother_name == dummy_value
    assert user.address == {dummy_value: dummy_value}
    assert user.portfolios == {dummy_value: dummy_value}
    assert user.identifier_document == {dummy_value: dummy_value}


@patch.object(Address, "build", side_effect=lambda **x: x)
@patch.object(UserPortfolios, "build", side_effect=lambda **x: x)
@patch.object(IdentifierDocument, "build", side_effect=lambda **x: x)
def test_instance_user_empty(mocked_build_document, mocked_build_portfolio, mocked_build_address):
    user = SnapshotUser.build(**stub_user_empty)
    assert user.email is None
    assert user.cel_phone is None
    assert user.birth_date is None
    assert user.mother_name is None
    assert user.address == {}
    assert user.portfolios == {}
    assert user.identifier_document == {}
