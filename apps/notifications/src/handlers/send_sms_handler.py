from src.configs.exceptions import OwnException
from src.handlers.base_api_handler import BaseApiHandler
from src.handlers.handlers_schemas import schema_sms
from src.handlers.http_decorators import validate_request
from src.notifications import sms
from src.setup import get_setup


class Handler(BaseApiHandler):
    @validate_request(schema_sms)
    def post(self, received_json):
        try:
            sms.send(
                received_json.get('sender') or get_setup().sms_credentials.phone_number,
                received_json['receiver'],
                received_json['body'],
                received_json['data'],
            )
        except OwnException as e:
            return self.send_failed(e.message)

        return self.send_success({})
