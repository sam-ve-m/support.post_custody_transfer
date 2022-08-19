from ...snapshot.model import Snapshot


class Warranty:
    @classmethod
    def build(cls, snapshot: Snapshot) -> dict:
        warranty_summary = snapshot.warranty
        snapshot = {
            "Disponível em Garantia": warranty_summary.available or "Sem definição",
        }
        return snapshot
