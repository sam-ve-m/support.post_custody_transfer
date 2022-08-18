from typing import List

from ..base.model import TableFromList
from ...snapshot.model import Snapshot
from ...snapshot.input.portfolio import Asset, Portfolio


class Wallet(TableFromList):
    wallet_name: str

    @classmethod
    def build(cls, snapshot: Snapshot):
        return cls(
            rows=cls.__get_wallets_assets(snapshot),
            columns=[
                "Código de bolsa",
                "Nome da carteira",
                "Ativo",
                "Preço Médio",
                "Quantidade",
                "Quantidade inicial",
                "Valor Gasto",
                "Valor Atual",
            ]
        )

    @classmethod
    def __get_wallets_assets(cls, snapshot: Snapshot):
        portfolio = snapshot.portfolio
        br_wallet_snapshot = cls._get_br_wallet(portfolio)
        us_wallet_snapshot = cls._get_us_wallet(portfolio)
        vnc_wallet_snapshot = cls._get_vnc_wallet(portfolio)
        wallets_assets = br_wallet_snapshot + us_wallet_snapshot + vnc_wallet_snapshot
        return wallets_assets

    @classmethod
    def _get_br_wallet(cls, portfolio: Portfolio) -> List[List[str]]:
        br_wallet_snapshot = cls.__get_assets(
            wallet=portfolio.wallet_br, wallet_name="Brazuca",
            wallet_id=portfolio.wallet_id_br.bovespa_account,
        )
        return br_wallet_snapshot

    @classmethod
    def _get_us_wallet(cls, portfolio: Portfolio) -> List[List[str]]:
        us_wallet_snapshot = cls.__get_assets(
            wallet=portfolio.wallet_us, wallet_name="Gringa",
            wallet_id=portfolio.wallet_id_us.dw_account,
        )
        return us_wallet_snapshot

    @classmethod
    def _get_vnc_wallet(cls, portfolio: Portfolio) -> List[List[str]]:
        vnc_wallet = []
        for _id, assets in portfolio.wallets_vnc_br.items():
            vnc_wallet_snapshot = cls.__get_assets(
                wallet_id=_id, wallet_name="Vai na Cola BR",
                wallet=assets)
            vnc_wallet.extend(vnc_wallet_snapshot)
        return vnc_wallet

    @classmethod
    def __get_assets(cls, wallet_id: str, wallet: List[Asset], wallet_name: str) -> List[List[str]]:
        normalized_wallet = [
            cls.__normalize_asset(asset, wallet_id, wallet_name)
            for asset in wallet
        ]
        return normalized_wallet

    @classmethod
    def __normalize_asset(cls, asset: Asset, wallet_id: str, wallet_name: str) -> List[str]:
        normalized_asset = [
            wallet_id,
            wallet_name,
            asset.ticker or "Exemplo",
            asset.mean_price or "Exemplo",
            asset.current_quantity or "Exemplo",
            asset.initial_quantity or "Exemplo",
            asset.spent_value or "Exemplo",
            asset.current_value or "Exemplo"
        ]
        return normalized_asset
