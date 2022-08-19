from ..base.model import TableFromList
from ...snapshot.model import Snapshot
from ...snapshot.input.portfolio import Asset


class WarrantyAssets(TableFromList):
    @classmethod
    def build(cls, snapshot: Snapshot) -> TableFromList:
        warranty_wallet = snapshot.portfolio.warranty
        warranty_assets = [cls.__normalize_assets(asset) for asset in warranty_wallet]
        snapshot = cls(columns=["Ativo", "Valor", "Quantidade"], rows=warranty_assets)
        return snapshot

    @staticmethod
    def __normalize_assets(asset: Asset) -> list:
        normalized_asset = [asset.ticker or "Sem definição",
                            asset.current_value or "Sem definição",
                            asset.current_quantity or "Sem definição"]
        return normalized_asset
