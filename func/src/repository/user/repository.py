from typing import Optional

from decouple import config
from etria_logger import Gladsheim

from ...domain.models.user import UserData
from ...infrastructure.mongo.infrastructure import MongoInfrastructure


class UserRepository:
    mongo_infra = MongoInfrastructure

    @classmethod
    def _get_collection(cls, collection: str):
        mongo_client = cls.mongo_infra.get_connection()
        user_mongodb_database = mongo_client.get_database(config("USER_MONGODB_DATABASE"))
        user_mongodb_collection = user_mongodb_database.get_collection(collection)
        return user_mongodb_collection

    @classmethod
    def find_user_by_unique_id(cls, unique_id: str) -> Optional[UserData]:
        collection = cls._get_collection(config("USER_MONGODB_COLLECTION"))
        try:
            user = collection.find_one({"unique_id": unique_id})
            return UserData(**user)
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Repository::find_user_by_unique_id::No record found with this unique_id::{unique_id}")
            raise ex
