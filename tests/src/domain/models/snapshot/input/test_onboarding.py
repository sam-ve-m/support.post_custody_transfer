from unittest.mock import patch

from src.domain.models.snapshot.input.onboarding import RegionStep, ReturnWrapper, OnboardingSteps

dummy_value = "value"
stub_region_step = {"current_step": dummy_value, "last_update_date": dummy_value}
stub_result_wrapper = {"result": {dummy_value: dummy_value}}
stub_onboarding_steps = {"br": {dummy_value: dummy_value}, "us": {dummy_value: dummy_value}}


def test_instance_region_step_with_content():
    region_step = RegionStep.build(**stub_region_step)
    assert region_step.current_step == dummy_value
    assert region_step.last_update_date == dummy_value


def test_instance_region_step_empty():
    region_step = RegionStep.build()
    assert region_step.current_step is None
    assert region_step.last_update_date is None


@patch.object(RegionStep, "build", side_effect=lambda **x: x)
def test_instance_result_wrapper_with_content(mocked_build):
    result_wrapper = ReturnWrapper.build(**stub_result_wrapper)
    assert result_wrapper.result == {dummy_value: dummy_value}


@patch.object(RegionStep, "build", side_effect=lambda **x: x)
def test_instance_result_wrapper_empty(mocked_build):
    result_wrapper = ReturnWrapper.build()
    assert result_wrapper.result == {}


@patch.object(ReturnWrapper, "build", side_effect=lambda **x: x)
def test_instance_onboarding_steps_with_content(mocked_build):
    onboarding_steps = OnboardingSteps.build(**stub_onboarding_steps)
    assert onboarding_steps.br == {dummy_value: dummy_value}
    assert onboarding_steps.us == {dummy_value: dummy_value}


@patch.object(ReturnWrapper, "build", side_effect=lambda **x: x)
def test_instance_onboarding_steps_empty(mocked_build):
    onboarding_steps = OnboardingSteps.build()
    assert onboarding_steps.br == {}
    assert onboarding_steps.us == {}
