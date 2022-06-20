# Jormungandr
from .tables.blocked_assets import BlockedAssetsTableBuilder
from .tables.onboarding import OnboardingTableBuilder
from .tables.pid import PIDTableBuilder
from .tables.user_blocks import UserBlocksTableBuilder
from .tables.vai_na_cola import VaiNaColaTableBuilder
from .tables.wallet import WalletTableBuilder
from .tables.warranty import WarrantyTableBuilder
from .tables.warranty_assets import WarrantyAssetsTableBuilder
from ...infrastructure.mongo.infrastructure import MongoInfrastructure
from ...infrastructure.snapshot.infrastructure import SnapshotInfrastructure


class SnapshotRepository:
    mongo_client = MongoInfrastructure.get_connection()
    snapshot_infrastructure = SnapshotInfrastructure

    @classmethod
    def snapshot_user_data(cls, jwt: str) -> str:
        snapshots = cls.snapshot_infrastructure.request_snapshot(jwt)
        snapshot = ("</br>"*2).join(filter(lambda x: x, (
            PIDTableBuilder.create_table(snapshots.pid)
            + OnboardingTableBuilder.create_table(snapshots.onboarding),

            WalletTableBuilder.create_table(snapshots.wallet),
            VaiNaColaTableBuilder.create_table(snapshots.vai_na_cola),

            BlockedAssetsTableBuilder.create_table(snapshots.blocked_assets)
            + UserBlocksTableBuilder.create_table(snapshots.user_blocks),

            WarrantyAssetsTableBuilder.create_table(snapshots.warranty_assets)
            + WarrantyTableBuilder.create_table(snapshots.warranty),
        )))
        return snapshot

