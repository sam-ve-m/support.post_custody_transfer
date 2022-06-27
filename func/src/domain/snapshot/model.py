from typing import List, Any
from pydantic import BaseModel


class Cell(BaseModel):
    label: str
    value: Any


Row = List[Cell]


class Snapshots(BaseModel):
    pid: List[Cell]
    onboarding: List[Row]
    wallet: List[Row]
    vai_na_cola: List[Row]
    blocked_assets: List[Row]
    user_blocks: List[Cell]
    warranty_assets: List[Row]
    warranty: List[Cell]
