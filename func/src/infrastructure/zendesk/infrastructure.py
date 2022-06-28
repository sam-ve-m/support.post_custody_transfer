from etria_logger import Gladsheim
from decouple import config
import zenpy


class ZendeskInfrastructure:
    client = None

    @classmethod
    def get_connection(cls):
        if cls.client is None:
            try:
                cls.client = zenpy.Zenpy(
                    email=config("ZENDESK_EMAIL"),
                    password=config("ZENDESK_PASSWORD"),
                    subdomain=config("ZENDESK_SUBDOMAIN"),
                )
            except Exception as ex:
                message = "_get_client::error to get Zenpy Client"
                Gladsheim.error(error=ex, message=message)
                raise ex
        return cls.client
