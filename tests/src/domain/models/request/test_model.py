# Standards
import re

# Jormungandr
from src.domain.models.request.model import Base64

# Third part
from unittest.mock import patch
from pydantic import validator
import pytest


dummy_content = "content"


@patch.object(re, "match", return_value=True)
def test_validate_content(mocked_regex):
    response = Base64.validate_content(dummy_content)
    assert response == dummy_content


@patch.object(re, "match", return_value=False)
def test_validate_content_invalid(mocked_regex):
    with pytest.raises(ValueError):
        Base64.validate_content(dummy_content)


def test_validate_content_environment():
    validator("content")(Base64.validate_content)

