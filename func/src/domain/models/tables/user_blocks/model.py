from ...snapshot.model import Snapshot
from ..base.model import TableFromList


class UserBlocks(TableFromList):
    @classmethod
    def build(cls, snapshot: Snapshot) -> dict:
        block_summary = snapshot.blocks
        date = block_summary.date or "Sem definição"
        block_type = block_summary.block_type or "Sem definição"
        description = block_summary.description or "Sem definição"
        lawsuit_number = block_summary.lawsuit_number or "Sem definição"
        snapshot = {
            "Data e Hora": date,
            "Descrição": description,
            "Tipo de bloqueio": block_type,
            "Numero do Processo (Caso bloqueio judicial)": lawsuit_number,
        }
        return snapshot
