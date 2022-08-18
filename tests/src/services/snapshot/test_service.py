from unittest.mock import MagicMock, patch

# Jormungandr
import pytest
from etria_logger import Gladsheim

from src.domain.builders.snapshot import HTMLSnapshotBuilder
from src.transport.jormungadr.transport import JormungandrTransport
from src.services.snapshot.service import SnapshotUserDataService
from src.domain.exceptions.exceptions import UnableToBuildSnapshot

dummy_jwt = "sd8a1f95dba9e85rza16s5d1vads"

dummy_html = "html"
dummy_empty_table = ""
dummy_snapshot = "snapshot"
fake_builder = MagicMock()
fake_builder.onboarding_table.return_value = fake_builder
fake_builder.line_break.return_value = fake_builder
fake_builder.wallet_table.return_value = fake_builder
fake_builder.vai_na_cola_table.return_value = fake_builder
fake_builder.blocked_assets_table.return_value = fake_builder
fake_builder.user_blocks_table.return_value = fake_builder
fake_builder.warranty_assets_table.return_value = fake_builder
fake_builder.warranty_table.return_value = fake_builder
fake_builder.build.return_value = dummy_html

dummy_exception = Exception("")
expected_message = "Error while building snapshot::"


@patch.object(Gladsheim, "error", return_value=fake_builder)
@patch.object(JormungandrTransport, "request_snapshot", return_value=dummy_snapshot)
@patch.object(HTMLSnapshotBuilder, "__init__", side_effect=dummy_exception)
@patch.object(HTMLSnapshotBuilder, "pid_table", return_value=fake_builder)
def test_unable_to_get_snapshot(mocked_builder_first_call, mocked_builder_instance,
                                mocked_transport, mocked_logger):
    with pytest.raises(UnableToBuildSnapshot):
        SnapshotUserDataService.get_snapshot(dummy_jwt)
    mocked_transport.assert_called_once_with(dummy_jwt)
    mocked_builder_instance.assert_called_once_with(dummy_snapshot)
    mocked_builder_first_call.assert_not_called()
    fake_builder.onboarding_table.assert_not_called()
    fake_builder.wallet_table.assert_not_called()
    fake_builder.vai_na_cola_table.assert_not_called()
    fake_builder.blocked_assets_table.assert_not_called()
    fake_builder.user_blocks_table.assert_not_called()
    fake_builder.warranty_assets_table.assert_not_called()
    fake_builder.warranty_table.assert_not_called()
    mocked_logger.assert_called_once_with(dummy_exception, message=expected_message)


@patch.object(Gladsheim, "error", return_value=fake_builder)
@patch.object(JormungandrTransport, "request_snapshot", return_value=dummy_snapshot)
@patch.object(HTMLSnapshotBuilder, "__init__", return_value=None)
@patch.object(HTMLSnapshotBuilder, "pid_table", return_value=fake_builder)
def test_get_snapshot(mocked_builder_first_call, mocked_builder_instance,
                      mocked_transport, mocked_logger):
    response = SnapshotUserDataService.get_snapshot(dummy_jwt)
    mocked_transport.assert_called_once_with(dummy_jwt)
    mocked_builder_instance.assert_called_once_with(dummy_snapshot)
    mocked_builder_first_call.assert_called_once_with()
    fake_builder.onboarding_table.assert_called_once_with()
    fake_builder.wallet_table.assert_called_once_with()
    fake_builder.vai_na_cola_table.assert_called_once_with()
    fake_builder.blocked_assets_table.assert_called_once_with()
    fake_builder.user_blocks_table.assert_called_once_with()
    fake_builder.warranty_assets_table.assert_called_once_with()
    fake_builder.warranty_table.assert_called_once_with()
    mocked_logger.assert_not_called()
    assert response == dummy_html
