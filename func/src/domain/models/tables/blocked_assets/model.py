from ..base.model import TableFromList
from ...snapshot.model import Snapshot
from ...snapshot.input.portfolio import Asset


class BlockedAssets(TableFromList):
    @classmethod
    def build(cls, snapshot: Snapshot):
        blocked_assets = snapshot.blocked_assets
        assets = [cls.__normalize_assets(asset) for asset in blocked_assets]
        snapshot = cls(
            columns=["Ativo", "Preço Médio", "Quantidade"],
            rows=assets
        )
        return snapshot

    @staticmethod
    def __normalize_assets(asset: Asset) -> list:
        normalized_asset = [
            asset.ticker or "Sem definição",
            asset.mean_price or "Sem definição",
            asset.current_quantity or "Sem definição",
        ]
        return normalized_asset
