from src.configs.exceptions import OwnException
from src.handlers.base_api_handler import BaseApiHandler
from src.handlers.handlers_schemas import schema_email
from src.handlers.http_decorators import validate_request
from src.notifications import email
from src.setup import get_setup


class Handler(BaseApiHandler):
    @validate_request(schema_email)
    def post(self, received_json):
        try:
            email.send(
                received_json.get('sender') or get_setup().email_credentials.email_sender,
                received_json['receiver'],
                received_json['subject'],
                received_json['text'],
                received_json['html'],
                received_json['pdfs'],
                received_json['data'],
            )
        except OwnException as e:
            return self.send_failed(e.message)

        return self.send_success({})
