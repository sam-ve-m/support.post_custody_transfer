# Standards
import re

# Third part
from pydantic import BaseModel, validator


class TicketValidator(BaseModel):
    stvm: str

    @validator("stvm", always=True, allow_reuse=True)
    def validate_stvm(cls, stvm):
        base_64_regex = r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$'
        if re.match(base_64_regex, stvm):
            return stvm
        raise ValueError("Base64 file content are invalid")


class Snapshots(BaseModel):
    pid: dict
    onboarding: list
    wallet: list
    vai_na_cola: list
    blocked_assets: list
    user_blocks: dict
    warranty_assets: list
    warranty: dict

