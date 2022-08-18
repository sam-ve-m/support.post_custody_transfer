class InvalidJwtToken(Exception):
    msg = "Failed to validate user credentials"


class JormungandrCommunication(Exception):
    msg = "Unable to communicate with other Jormungandr fission"


class ErrorWithZendesk(Exception):
    msg = "Unable to execute an action in Zendesk"


class UnableToBuildSnapshot(Exception):
    msg = "Error while building snapshot"
