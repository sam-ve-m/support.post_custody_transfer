from http import HTTPStatus

import requests
from decouple import config

from ...domain.models.snapshot.model import Snapshot
from ...domain.exceptions.exceptions import JormungandrCommunication


class JormungandrTransport:
    @classmethod
    def request_snapshot(cls, jwt: str) -> Snapshot:
        url = config("JORMUNGANDR_GET_USER_SNAPSHOT")
        try:
            snapshot_response = requests.get(url, headers={"x-thebes-answer": jwt})
        except Exception as error:
            raise JormungandrCommunication(str(error))
        if snapshot_response.status_code != HTTPStatus.OK:
            raise JormungandrCommunication(f"""Fail obtaining Snapshots 
                Status Code: {snapshot_response.status_code}
                Content: {snapshot_response.content}
            """)
        snapshot_json = snapshot_response.json()
        snapshot = snapshot_json.get("result")
        return Snapshot.build(**snapshot)

    @classmethod
    def update_ticket_with_comment(cls, jwt: str, ticket_id: int, comment: str) -> bool:
        url = config("JORMUNGANDR_UPDATE_TICKET_COMMENT")
        try:
            snapshot_response = requests.put(
                url,
                json={"body": comment, "id": ticket_id},
                headers={"x-thebes-answer": jwt},
            )
        except Exception as error:
            raise JormungandrCommunication(str(error))
        if snapshot_response.status_code != HTTPStatus.OK:
            raise JormungandrCommunication(f"""Fail updating Ticket with a Comment 
                Status Code: {snapshot_response.status_code}
                Content: {snapshot_response.content}
            """)
        return True
