from dataclasses import dataclass


@dataclass
class DocumentData:
    number: str = None

    @classmethod
    def from_dict(cls, document: dict):
        if not document:
            return cls()
        return cls(number=document.get("number"))


@dataclass
class IdentifierDocument:
    cpf: str
    document_data: DocumentData

    @classmethod
    def build(cls, cpf: str = None, document_data: dict = None):
        return cls(
            cpf=cpf,
            document_data=DocumentData.from_dict(document_data),
        )


@dataclass
class VncPortfolio:
    br: str = None

    @classmethod
    def from_dict(cls, vnc: dict):
        if not vnc:
            return cls()
        return cls(**vnc)


@dataclass
class UserPortfolios:
    vnc: VncPortfolio

    @classmethod
    def build(cls, vnc: dict = None):
        return cls(vnc=VncPortfolio.from_dict(vnc))


@dataclass
class Address:
    zip_code: str

    @classmethod
    def build(cls, zip_code: str = None, **kwargs):
        return cls(zip_code=zip_code)


@dataclass
class SnapshotUser:
    email: str
    cel_phone: str
    birth_date: str
    mother_name: str
    address: Address
    portfolios: UserPortfolios
    identifier_document: IdentifierDocument

    @classmethod
    def build(
            cls,
            email: str,
            birth_date: str,
            mother_name: str,
            cel_phone: str = None,
            address: dict = None,
            portfolios: dict = None,
            identifier_document: dict = None,
            **kwargs,
    ):
        return cls(
            email=email,
            cel_phone=cel_phone,
            birth_date=birth_date,
            mother_name=mother_name,
            address=Address.build(**({} if address is None else address)),
            portfolios=UserPortfolios.build(**({} if portfolios is None else portfolios)),
            identifier_document=IdentifierDocument.build(**({} if identifier_document is None else identifier_document))
        )
