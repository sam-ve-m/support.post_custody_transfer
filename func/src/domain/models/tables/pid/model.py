from ...snapshot.input.user import SnapshotUser
from ...snapshot.model import Snapshot


class PID:
    NOT_FOUND_MESSAGE = "Não encontrado"

    @classmethod
    def build(cls, snapshot: Snapshot) -> dict:
        user_data = snapshot.user
        cpf = cls.__set_cpf_in_snapshot(user_data)
        email = cls.__set_email_in_snapshot(user_data)
        has_vai_na_cola = bool(user_data.portfolios.vnc.br)
        cellphone = user_data.cel_phone or cls.NOT_FOUND_MESSAGE
        birth_date = user_data.birth_date or cls.NOT_FOUND_MESSAGE
        cep = user_data.address.zip_code or cls.NOT_FOUND_MESSAGE
        mothers_name = user_data.mother_name or cls.NOT_FOUND_MESSAGE
        rg = user_data.identifier_document.document_data.number or cls.NOT_FOUND_MESSAGE
        snapshot = {
            "RG": rg,
            "CEP": cep,
            "Cpf": cpf,
            "Email": email,
            "Telefone": cellphone,
            "Nome da Mãe": mothers_name,
            "Data Nascimento": birth_date,
            "Possui Vai na Cola?": has_vai_na_cola,
        }
        return snapshot

    @staticmethod
    def __set_email_in_snapshot(user_data: SnapshotUser) -> str:
        if not (email := user_data.email):
            raise ValueError("Email field is required. Not returned from jormungandr snapshot.")
        return email

    @staticmethod
    def __set_cpf_in_snapshot(user_data: SnapshotUser) -> str:
        if not (cpf := user_data.identifier_document.cpf):
            raise ValueError("Cpf field is required. Not returned from jormungandr snapshot.")
        return cpf
