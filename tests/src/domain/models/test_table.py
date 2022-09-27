import pytest
from dataclasses import FrozenInstanceError
from src.domain.models.tables.base.model import TableFromList

dummy_value = "dummy"


def test_fronzen():
    model = TableFromList(dummy_value, dummy_value)
    with pytest.raises(FrozenInstanceError):
        model.columns = dummy_value
