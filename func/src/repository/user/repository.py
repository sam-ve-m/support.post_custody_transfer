from etria_logger import Gladsheim
from typing import Optional
from decouple import config

from ...infrastructure.mongo.infrastructure import MongoInfrastructure


class UserRepository:
    mongo_client = MongoInfrastructure.get_connection()

    @classmethod
    def __get_collection(cls, collection: dict):
        user_mongodb_database = cls.mongo_client.get_database(config("USER_MONGODB_DATABASE"))
        user_mongodb_collection = user_mongodb_database.get_collection(collection)
        return user_mongodb_collection

    @classmethod
    def find_user_by_unique_id(cls, unique_id: str) -> Optional[dict]:
        collection = cls.__get_collection(config("USER_MONGODB_COLLECTION"))
        try:
            user = collection.find_one({"unique_id": unique_id})
            return user
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Repository::find_user_by_unique_id::No record found with this unique_id::{unique_id}")
            raise ex
