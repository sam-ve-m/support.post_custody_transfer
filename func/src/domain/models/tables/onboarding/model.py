from ..base.model import TableFromList
from ...snapshot.model import Snapshot
from ...snapshot.input.onboarding import OnboardingSteps


class Onboarding(TableFromList):
    MISSING_STEP = "Não Iniciado"
    MISSING_DATE = "??/??/????"

    @classmethod
    def build(cls, snapshot: Snapshot):
        onboarding_steps = snapshot.onboarding_steps
        snapshot = cls(
            columns=["Campo", "BR", "US"],
            rows=[
                cls.__current_steps(onboarding_steps),
                cls.__current_steps_last_update(onboarding_steps),
            ]
        )
        return snapshot

    @classmethod
    def __current_steps(cls, onboarding_steps: OnboardingSteps) -> list:
        missed_steps_br = onboarding_steps.br.result.current_step or cls.MISSING_STEP
        missed_steps_us = onboarding_steps.us.result.current_step or cls.MISSING_STEP
        missed_steps = ["Faltou fazer", missed_steps_br, missed_steps_us]
        return missed_steps

    @classmethod
    def __current_steps_last_update(cls, onboarding_steps: OnboardingSteps) -> list:
        date_br = onboarding_steps.br.result.last_update_date or cls.MISSING_DATE
        date_us = onboarding_steps.us.result.last_update_date or cls.MISSING_DATE
        dates = ["Data da Ultima", date_br, date_us]
        return dates
