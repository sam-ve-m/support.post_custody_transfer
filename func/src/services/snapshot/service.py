# Jormungandr
from ...domain.builders.snapshot import HTMLSnapshotBuilder
from ...transport.jormungadr.transport import JormungandrTransport
from ...domain.exceptions.exceptions import UnableToBuildSnapshot

from etria_logger import Gladsheim


class SnapshotUserDataService:
    @classmethod
    def get_snapshot(cls, jwt: str) -> str:
        snapshots = JormungandrTransport.request_snapshot(jwt)
        try:
            snapshot_html = (HTMLSnapshotBuilder(snapshots)
                             .pid_table()
                             .onboarding_table()
                             .wallet_table()
                             .vai_na_cola_table()
                             .blocked_assets_table()
                             .user_blocks_table()
                             .warranty_assets_table()
                             .warranty_table()
                             ).build()
            return snapshot_html
        except Exception as error:
            Gladsheim.error(error, message="::".join((UnableToBuildSnapshot.msg, str(error))))
            raise UnableToBuildSnapshot()

