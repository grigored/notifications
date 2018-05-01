from src.configs.exceptions import OwnException
from src.handlers.base_api_handler import BaseApiHandler
from src.handlers.handlers_schemas import schema_notification
from src.handlers.http_decorators import validate_request
from src.notifications import email, sms
from src.setup import get_setup


class Handler(BaseApiHandler):
    @validate_request(schema_notification)
    def post(self, received_json):
        try:
            email_details = received_json.get('email')
            if email_details:
                email.send(
                    email_details.get('sender') or get_setup().email_credentials.email_sender,
                    email_details['receiver'],
                    email_details['email_subject_template'],
                    email_details['email_text_template'],
                    email_details['email_html_template'],
                    email_details['pdfs'],
                    email_details['data'],
                )

            sms_details = received_json.get('sms')
            if sms_details:
                sms.send(
                    sms_details.get('sender') or get_setup().sms_credentials.phone_number,
                    sms_details['receiver'],
                    sms_details['sms_template'],
                    sms_details['data'],
                )
        except OwnException as e:
            return self.send_failed(e.message)

        return self.send_success({})
