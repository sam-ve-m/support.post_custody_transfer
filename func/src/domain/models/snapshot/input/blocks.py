from dataclasses import dataclass


@dataclass
class Blocks:
    date: str = None
    block_type: str = None
    description: str = None
    lawsuit_number: str = None

    @classmethod
    def from_dict(cls, blocks: dict):
        if not blocks:
            return cls()
        return cls(**blocks)
