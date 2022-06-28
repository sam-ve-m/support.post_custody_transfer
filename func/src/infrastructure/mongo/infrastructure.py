from etria_logger import Gladsheim
from decouple import config
import pymongo


class MongoInfrastructure:
    client = None

    @classmethod
    def get_connection(cls):
        if cls.client is None:
            try:
                cls.client = pymongo.MongoClient(config("MONGO_CLIENT_URL"))
            except Exception as ex:
                Gladsheim.error(
                    error=ex,
                    message=f"MongoInfrastructure::get_connection::Error trying to get Mongo Client",
                )
                raise ex
        return cls.client
