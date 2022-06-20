from etria_logger import Gladsheim
from pymongo import MongoClient
from decouple import config


class MongoInfrastructure:
    client = None

    @classmethod
    def get_connection(cls):
        if cls.client is None:
            try:
                cls.client = MongoClient(config("MONGO_CLIENT_URL"))
            except Exception as ex:
                Gladsheim.error(
                    error=ex,
                    message=f"MongoInfrastructure::get_connection::Error trying to get Mongo Client",
                )
                raise ex
        return cls.client
