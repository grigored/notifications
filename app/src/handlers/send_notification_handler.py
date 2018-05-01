from src.handlers.base_api_handler import BaseApiHandler
from src.handlers.http_decorators import validate_request
from src.handlers.handlers_schemas import schema_notification
from src.notifications import email
from src.setup import get_setup


class SendNotificationHandler(BaseApiHandler):
    @validate_request(schema_notification)
    def post(self, received_json):
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
            pass
        return self.send_success({})
