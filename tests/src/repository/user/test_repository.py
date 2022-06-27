from unittest.mock import MagicMock, patch

import pytest
from decouple import AutoConfig
from etria_logger import Gladsheim

from func.src.repository.user.repository import UserRepository

dummy_collection = {}
fake_collection = MagicMock()
fake_database = MagicMock()
fake_database.get_collection.return_value = fake_collection
fake_client = MagicMock()
fake_client.get_database.return_value = fake_database
fake_infra = MagicMock()
fake_infra.get_connection.return_value = fake_client


@patch.object(AutoConfig, "__call__")
def test_get_collection(mocked_env, monkeypatch):
    monkeypatch.setattr(UserRepository, "mongo_infra", fake_infra)
    response = UserRepository._get_collection(dummy_collection)
    assert response == fake_collection


dummy_unique_id = 159159


@patch.object(AutoConfig, "__call__")
@patch.object(UserRepository, "_get_collection", return_value=fake_collection)
def test_find_user_by_unique_id(mocked_collection_getter, mocked_env):
    fake_collection.find_one = MagicMock(return_value=dummy_collection)
    response = UserRepository.find_user_by_unique_id(dummy_unique_id)
    fake_collection.find_one.assert_called_once_with({"unique_id": dummy_unique_id})
    assert response == dummy_collection


dummy_exception = ValueError()


@patch.object(Gladsheim, "error")
@patch.object(AutoConfig, "__call__")
@patch.object(UserRepository, "_get_collection", return_value=fake_collection)
def test_find_user_by_unique_id(mocked_collection_getter, mocked_env, mocked_logger):
    fake_collection.find_one = MagicMock(side_effect=dummy_exception)
    with pytest.raises(dummy_exception.__class__):
        UserRepository.find_user_by_unique_id(dummy_unique_id)
    fake_collection.find_one.assert_called_once_with({"unique_id": dummy_unique_id})
