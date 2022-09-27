from typing import List
from unittest.mock import MagicMock

import pytest

from src.domain.models.tables.onboarding.model import Onboarding

dummy_step = "Step"
dummy_date = "Date"
dummy_missing_date = "??/??/????"
dummy_missing_step = "Não Iniciado"
expected_columns = ["Campo", "BR", "US"]

nothing_missing = MagicMock(
    br=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date)),
    us=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date))
), [["Faltou fazer", dummy_step, dummy_step], ["Data da Ultima", dummy_date, dummy_date]]

all_missing = MagicMock(
    br=MagicMock(result=MagicMock(current_step=None, last_update_date=None)),
    us=MagicMock(result=MagicMock(current_step=None, last_update_date=None))
), [["Faltou fazer", dummy_missing_step, dummy_missing_step], ["Data da Ultima", dummy_missing_date, dummy_missing_date]]
br_missing = MagicMock(
    br=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date)),
    us=MagicMock(result=MagicMock(current_step=None, last_update_date=None))
), [["Faltou fazer", dummy_step, dummy_missing_step], ["Data da Ultima", dummy_date, dummy_missing_date]]
us_missing = MagicMock(
    br=MagicMock(result=MagicMock(current_step=None, last_update_date=None)),
    us=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date))
), [["Faltou fazer", dummy_missing_step, dummy_step], ["Data da Ultima", dummy_missing_date, dummy_date]]


all_missing_date = MagicMock(
    br=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=None)),
    us=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=None))
), [["Faltou fazer", dummy_step, dummy_step], ["Data da Ultima", dummy_missing_date, dummy_missing_date]]
br_missing_date = MagicMock(
    br=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date)),
    us=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=None))
), [["Faltou fazer", dummy_step, dummy_step], ["Data da Ultima", dummy_date, dummy_missing_date]]
us_missing_date = MagicMock(
    br=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=None)),
    us=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date))
), [["Faltou fazer", dummy_step, dummy_step], ["Data da Ultima", dummy_missing_date, dummy_date]]


all_missing_step = MagicMock(
    br=MagicMock(result=MagicMock(current_step=None, last_update_date=dummy_date)),
    us=MagicMock(result=MagicMock(current_step=None, last_update_date=dummy_date))
), [["Faltou fazer", dummy_missing_step, dummy_missing_step], ["Data da Ultima", dummy_date, dummy_date]]
br_missing_step = MagicMock(
    br=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date)),
    us=MagicMock(result=MagicMock(current_step=None, last_update_date=dummy_date))
), [["Faltou fazer", dummy_step, dummy_missing_step], ["Data da Ultima", dummy_date, dummy_date]]
us_missing_step = MagicMock(
    br=MagicMock(result=MagicMock(current_step=None, last_update_date=dummy_date)),
    us=MagicMock(result=MagicMock(current_step=dummy_step, last_update_date=dummy_date))
), [["Faltou fazer", dummy_missing_step, dummy_step], ["Data da Ultima", dummy_date, dummy_date]]


@pytest.mark.parametrize("dummy_onboarding_steps,expected_rows", [
    nothing_missing, all_missing, br_missing, us_missing,
    all_missing_date, br_missing_date, us_missing_date,
    all_missing_step, br_missing_step, us_missing_step,
])
def test_get_snapshot(dummy_onboarding_steps: dict, expected_rows: List[list]):
    response = Onboarding.build(MagicMock(onboarding_steps=dummy_onboarding_steps))
    assert response.rows == expected_rows and response.columns == expected_columns
