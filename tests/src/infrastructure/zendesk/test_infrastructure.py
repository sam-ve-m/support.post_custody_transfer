from unittest.mock import patch

import zenpy
import pytest
from decouple import AutoConfig
from etria_logger import Gladsheim

from func.src.infrastructure.zendesk.infrastructure import ZendeskInfrastructure

dummy_connection = "dummy connection"


@patch.object(AutoConfig, "__call__")
@patch.object(zenpy, "Zenpy", return_value=dummy_connection)
def test_get_connection(mock_s3_connection, mocked_env):
    new_connection_created = ZendeskInfrastructure.get_connection()
    assert new_connection_created == dummy_connection
    mock_s3_connection.assert_called_once()

    reused_client = ZendeskInfrastructure.get_connection()
    assert reused_client == new_connection_created
    mock_s3_connection.assert_called_once()
    ZendeskInfrastructure.client = None


stub_error = AssertionError()


@patch.object(Gladsheim, "error")
@patch.object(AutoConfig, "__call__")
@patch.object(zenpy, "Zenpy", side_effect=stub_error)
def test_get_connection_with_error(mock_s3_connection, mocked_env, mocked_logger):
    with pytest.raises(stub_error.__class__):
        ZendeskInfrastructure.get_connection()
    mocked_logger.assert_called_once()
