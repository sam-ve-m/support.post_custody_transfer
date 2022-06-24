from http import HTTPStatus

import requests
from decouple import config

from ...domain.snapshot.model import Snapshots


class SnapshotRepository:
    @classmethod
    def request_snapshot(cls, jwt: str) -> Snapshots:
        snapshot_response = requests.get(config("JORMUNGANDR_GET_USER_SNAPSHOT"), headers={"x-thebes-answer": jwt})
        if snapshot_response.status_code != HTTPStatus.OK:
            raise ValueError("Falha ao obter Snapshots")  # TODO: Melhorar erro
        snapshot_json = snapshot_response.json()
        snapshot = Snapshots(**snapshot_json.get("result"))
        return snapshot
