from .base.create_table import BaseTableBuilder
from ..models.snapshot.model import Snapshot
from ..models.tables.blocked_assets.model import BlockedAssets
from ..models.tables.onboarding.model import Onboarding
from ..models.tables.pid.model import PID
from ..models.tables.user_blocks.model import UserBlocks
from ..models.tables.vai_na_cola.model import VaiNaColaReport
from ..models.tables.wallet.model import Wallet
from ..models.tables.warranty.model import Warranty
from ..models.tables.warranty_assets.model import WarrantyAssets


class HTMLSnapshotBuilder(BaseTableBuilder):
    def __init__(self, snapshot: Snapshot):
        self.__snapshot = snapshot
        self.__pid_html_table = ""
        self.__wallet_html_table = ""
        self.__warranty_html_table = ""
        self.__onboarding_html_table = ""
        self.__vai_na_cola_html_table = ""
        self.__user_blocks_html_table = ""
        self.__blocked_assets_html_table = ""
        self.__warranty_assets_html_table = ""

    def pid_table(self):
        pid_snapshot = PID.build(self.__snapshot)
        self.__pid_html_table = self._create_table_from_dict(pid_snapshot,
                                                             table_name="PID",
                                                             color="black")
        return self

    def onboarding_table(self):
        onboarding_snapshot = Onboarding.build(self.__snapshot)
        self.__onboarding_html_table = self._create_table_from_list(onboarding_snapshot,
                                                                    table_name="Onboarding",
                                                                    color="black")
        return self

    def wallet_table(self):
        wallet = Wallet.build(self.__snapshot)
        self.__wallet_html_table = self._create_table_from_list(wallet,
                                                                table_name="Carteira",
                                                                color="purple")
        return self

    def vai_na_cola_table(self):
        vai_na_cola_snapshot = VaiNaColaReport.build(self.__snapshot)
        self.__vai_na_cola_html_table = self._create_table_from_list(vai_na_cola_snapshot,
                                                                     table_name="Vai na Cola",
                                                                     color="darkgreen")
        return self

    def blocked_assets_table(self):
        blocked_assets_snapshot = BlockedAssets.build(self.__snapshot)
        self.__blocked_assets_html_table = self._create_table_from_list(blocked_assets_snapshot,
                                                                        table_name="Ativos Bloqueados",
                                                                        color="darkred")
        return self

    def user_blocks_table(self):
        user_blocks_snapshot = UserBlocks.build(self.__snapshot)
        self.__user_blocks_html_table = self._create_table_from_dict(user_blocks_snapshot,
                                                                     table_name="Bloqueio",
                                                                     color="darkred")
        return self

    def warranty_assets_table(self):
        warranty_assets_snapshot = WarrantyAssets.build(self.__snapshot)
        self.__warranty_assets_html_table = self._create_table_from_list(warranty_assets_snapshot,
                                                                         table_name="Ativos Em Garantia",
                                                                         color="darkblue")
        return self

    def warranty_table(self):
        warranty_snapshot = Warranty.build(self.__snapshot)
        self.__warranty_html_table = self._create_table_from_dict(warranty_snapshot,
                                                                  table_name="Garantia",
                                                                  color="darkblue")
        return self

    def build(self) -> str:
        html = "</br>".join(filter(bool, (
            " ".join(filter(bool, (
                self.__pid_html_table,
                self.__onboarding_html_table,
            ))),
            self.__wallet_html_table,
            self.__vai_na_cola_html_table,
            " ".join(filter(bool, (
                self.__user_blocks_html_table,
                self.__blocked_assets_html_table,
            ))),
            " ".join(filter(bool, (
                self.__warranty_html_table,
                self.__warranty_assets_html_table,
            ))),
        )))
        return html
