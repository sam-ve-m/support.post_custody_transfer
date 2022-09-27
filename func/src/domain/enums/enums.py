# Standards
from enum import Enum, IntEnum


class CodeResponse(IntEnum):
    SUCCESS = 0
    JWT_INVALID = 30
    INVALID_PARAMS = 10
    INTERNAL_SERVER_ERROR = 100
    PARTNERS_ERROR_ON_API_REQUEST = 21


class TicketType(Enum):
    PROBLEM = "problem"
    INCIDENT = "incident"
    QUESTION = "question"
    TASK = "task"
