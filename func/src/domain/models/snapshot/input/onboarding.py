from dataclasses import dataclass


@dataclass
class RegionStep:
    current_step: str
    last_update_date: str

    @classmethod
    def build(cls, current_step: str = None, last_update_date: str = None, **kwargs):
        return cls(
            last_update_date=last_update_date,
            current_step=current_step,
        )


@dataclass
class ReturnWrapper:
    result: RegionStep

    @classmethod
    def build(cls, result: dict = None, **kwargs):
        return cls(result=RegionStep.build(**({} if result is None else result)))


@dataclass
class OnboardingSteps:
    br: ReturnWrapper
    us: ReturnWrapper

    @classmethod
    def build(cls, br: dict = None, us: dict = None):
        return cls(
            br=ReturnWrapper.build(**({} if br is None else br)),
            us=ReturnWrapper.build(**({} if us is None else us)),
        )
