# Jormungandr
from ..domain.snapshot.html.tables.blocked_assets import BlockedAssetsTableDTO
from ..domain.snapshot.html.tables.onboarding import OnboardingTableDTO
from ..domain.snapshot.html.tables.pid import PIDTableDTO
from ..domain.snapshot.html.tables.user_blocks import UserBlocksTableDTO
from ..domain.snapshot.html.tables.vai_na_cola import VaiNaColaTableDTO
from ..domain.snapshot.html.tables.wallet import WalletTableDTO
from ..domain.snapshot.html.tables.warranty import WarrantyTableDTO
from ..domain.snapshot.html.tables.warranty_assets import WarrantyAssetsTableDTO
from ..repository.snapshot.repository import SnapshotRepository


class SnapshotUserDataService:
    snapshot_repository = SnapshotRepository

    @classmethod
    def get_snapshot(cls, jwt: str) -> str:
        snapshots = cls.snapshot_repository.request_snapshot(jwt)
        snapshot = "</br></br>".join(filter(lambda x: x, (
            "".join((PIDTableDTO.create_table(snapshots.pid),
                     OnboardingTableDTO.create_table(snapshots.onboarding))),

            WalletTableDTO.create_table(snapshots.wallet),
            VaiNaColaTableDTO.create_table(snapshots.vai_na_cola),

            "".join((BlockedAssetsTableDTO.create_table(snapshots.blocked_assets),
                     UserBlocksTableDTO.create_table(snapshots.user_blocks))),

            "".join((WarrantyAssetsTableDTO.create_table(snapshots.warranty_assets),
                     WarrantyTableDTO.create_table(snapshots.warranty))),
        )))
        return snapshot
