from src.domain.models.snapshot.input.portfolio import Portfolio, Asset
from src.domain.models.snapshot.input.onboarding import OnboardingSteps
from src.domain.models.snapshot.input.warranty import WarrantyResume
from src.domain.models.snapshot.input.user import SnapshotUser
from src.domain.models.snapshot.input.blocks import Blocks
from src.domain.models.snapshot.model import Snapshot
from unittest.mock import patch


dummy_value = "value"
stub_snapshot = {
    "user": {dummy_value: dummy_value},
    "portfolio": {dummy_value: dummy_value},
    "onboarding_steps": {dummy_value: dummy_value},
    "blocks": dummy_value,
    "warranty": {dummy_value: dummy_value},
    "blocked_assets": [dummy_value, dummy_value],
}
stub_snapshot_empty = {
    "user": {},
    "portfolio": {},
    "onboarding_steps": {},
}


@patch.object(SnapshotUser, "build", side_effect=lambda **x: x)
@patch.object(Blocks, "from_dict", side_effect=lambda x: x)
@patch.object(Portfolio, "build", side_effect=lambda **x: x)
@patch.object(WarrantyResume, "__init__", return_value=None)
@patch.object(Asset, "from_dict", side_effect=lambda x: x)
@patch.object(OnboardingSteps, "build", side_effect=lambda **x: x)
def test_instance_snapshot_with_content(
    mocked_onboarding_steps,
    mocked_asset,
    mocked_warranty,
    mocked_portfolio,
    mocked_blocks,
    mocked_snapshot_user,
):
    snapshot = Snapshot.build(**stub_snapshot)
    assert snapshot.user == {dummy_value: dummy_value}
    assert snapshot.portfolio == {dummy_value: dummy_value}
    assert snapshot.onboarding_steps == {dummy_value: dummy_value}
    mocked_warranty.assert_called_once_with(**{dummy_value: dummy_value})
    assert snapshot.blocks == dummy_value
    assert snapshot.blocked_assets == [dummy_value, dummy_value]


@patch.object(SnapshotUser, "build", side_effect=lambda **x: x)
@patch.object(Blocks, "from_dict", side_effect=lambda x: x)
@patch.object(Portfolio, "build", side_effect=lambda **x: x)
@patch.object(WarrantyResume, "__init__", return_value=None)
@patch.object(Asset, "from_dict", side_effect=lambda x: x)
@patch.object(OnboardingSteps, "build", side_effect=lambda **x: x)
def test_instance_snapshot_empty(
    mocked_onboarding_steps,
    mocked_asset,
    mocked_warranty,
    mocked_portfolio,
    mocked_blocks,
    mocked_snapshot_user,
):
    snapshot = Snapshot.build(**stub_snapshot_empty)
    assert snapshot.user == {}
    assert snapshot.portfolio == {}
    assert snapshot.onboarding_steps == {}
    mocked_warranty.assert_called_once_with()
    assert snapshot.blocks is None
    assert snapshot.blocked_assets == []
