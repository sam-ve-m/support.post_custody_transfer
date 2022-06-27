# Standards
import re
from typing import List

# Third part
from pydantic import BaseModel, validator


class Base64(BaseModel):
    name: str
    content: str

    @validator("content", allow_reuse=True)
    def validate_content(cls, content):
        base_64_regex = r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$'
        if re.match(base_64_regex, content):
            return content
        raise ValueError("Base64 file content are invalid")


class TicketValidator(BaseModel):
    attachments: List[Base64]
