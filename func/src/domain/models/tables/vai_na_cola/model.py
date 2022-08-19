from typing import List
from ..base.model import TableFromList
from ...snapshot.input.portfolio import VaiNaColaWalletReport
from ...snapshot.model import Snapshot


class VaiNaColaReport(TableFromList):
    @classmethod
    def build(cls, snapshot: Snapshot) -> TableFromList:
        vnc_portfolio_report = snapshot.portfolio.wallets_vnc_br_report
        snapshot = cls(
            columns=[
                "Carteira/Código",
                "Influencer",
                "Tipo Influencer",
                "Data de referência",
                "Rentabilidade Vai na Cola",
                "Desenquadrado"
            ],
            rows=cls.__normalize_vnc_portfolio_report(vnc_portfolio_report)
        )
        return snapshot

    @classmethod
    def __normalize_vnc_portfolio_report(cls, vnc_portfolio_report: List[VaiNaColaWalletReport]) -> list:
        normalized_vnc_portfolio_report = [
            cls.__normalize_vnc_wallet_report(wallet_report)
            for wallet_report in vnc_portfolio_report
        ]
        return normalized_vnc_portfolio_report

    @staticmethod
    def __normalize_vnc_wallet_report(wallet_report: VaiNaColaWalletReport) -> list:
        normalized_vnc_wallet_report = [
            wallet_report.id,
            "Pendente de Definição",
            "Pendente de Definição",
            "Pendente de Definição",
            "Pendente de Definição",
            "Pendente de Definição",
        ]
        return normalized_vnc_wallet_report
