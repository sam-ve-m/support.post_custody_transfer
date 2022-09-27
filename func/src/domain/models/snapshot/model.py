from typing import List
from .input.blocks import Blocks
from .input.user import SnapshotUser
from .input.warranty import WarrantyResume
from .input.portfolio import Portfolio, Asset
from .input.onboarding import OnboardingSteps
from dataclasses import dataclass


@dataclass
class Snapshot:
    blocks: Blocks
    user: SnapshotUser
    portfolio: Portfolio
    warranty: WarrantyResume
    blocked_assets: List[Asset]
    onboarding_steps: OnboardingSteps

    @classmethod
    def build(
            cls,
            user: dict,
            portfolio: dict,
            onboarding_steps: dict,
            blocks: dict = None,
            warranty: dict = None,
            blocked_assets: dict = None,
            **kwargs
    ):
        user = SnapshotUser.build(**user)
        blocks = Blocks.from_dict(blocks)
        portfolio = Portfolio.build(**portfolio)
        warranty = WarrantyResume(**({} if warranty is None else warranty))
        blocked_assets = [Asset.from_dict(asset) for asset in ([] if blocked_assets is None else blocked_assets)]
        onboarding_steps = OnboardingSteps.build(**onboarding_steps)
        return cls(
            user=user,
            blocks=blocks,
            portfolio=portfolio,
            warranty=warranty,
            blocked_assets=blocked_assets,
            onboarding_steps=onboarding_steps,
        )
