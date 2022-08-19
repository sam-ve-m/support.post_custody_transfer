from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TableFromList:
    columns: List[str]
    rows: List[List[str]]
