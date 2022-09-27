from dataclasses import dataclass
from typing import List, Dict


@dataclass
class PortfolioWalletBR:
    bmf_account: str
    bovespa_account: str

    @classmethod
    def build(cls, bmf_account: str = None, bovespa_account: str = None, **kwargs):
        return cls(bovespa_account=bovespa_account, bmf_account=bmf_account)


@dataclass
class PortfolioWalletUS:
    dw_account: str

    @classmethod
    def build(cls, dw_account: str = None, **kwargs):
        return cls(dw_account=dw_account)


@dataclass
class Asset:
    ticker: str = None
    mean_price: float = None
    spent_value: float = None
    current_value: float = None
    current_quantity: int = None
    initial_quantity: int = None

    @classmethod
    def from_dict(cls, asset: dict):
        if not asset:
            return cls()
        return cls(**asset)


@dataclass
class VaiNaColaWalletReport:
    id: str


@dataclass
class Portfolio:
    warranty: List[Asset]
    wallet_us: List[Asset]
    wallet_br: List[Asset]
    wallet_id_br: PortfolioWalletBR
    wallet_id_us: PortfolioWalletUS
    wallets_vnc_br: Dict[str, List[Asset]]
    wallets_vnc_br_report: List[VaiNaColaWalletReport]

    @classmethod
    def build(
            cls,
            wallet_id_br: dict,
            wallet_id_us: dict,
            wallet_us: List[dict],
            wallet_br: List[dict],
            wallets_vnc_br: Dict[str, List[dict]],
            wallets_vnc_br_report: List[dict] = None,
            warranty: List[dict] = None,
    ):
        if wallets_vnc_br_report is None:
            wallets_vnc_br_report = [{"id": _id} for _id in wallets_vnc_br]
        for _id in wallets_vnc_br:
            wallets_vnc_br[_id] = [{}]
        return cls(
            warranty=[Asset.from_dict(asset) for asset in ([] if warranty is None else warranty)],
            wallet_us=[Asset.from_dict(asset) for asset in wallet_us or ([{}] if wallet_id_us else [])],
            wallet_br=[Asset.from_dict(asset) for asset in wallet_br or ([{}] if wallet_id_br else [])],
            wallet_id_br=PortfolioWalletBR.build(**(wallet_id_br or {})),
            wallet_id_us=PortfolioWalletUS.build(**(wallet_id_us or {})),
            wallets_vnc_br_report=[VaiNaColaWalletReport(**report) for report in wallets_vnc_br_report],
            wallets_vnc_br={_id: [Asset.from_dict(asset) for asset in assets]
                            for _id, assets in wallets_vnc_br.items()},
        )
