import logging
import typing

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from src.configs.exceptions import OwnException
from src.configs.strings import SMS_NOT_CONFIGURED, SMS_COULD_NOT_BE_SENT, TWILIO_NOT_SETUP
from src.notifications.template import build_template
from src.setup import get_setup

__twilio_singleton: typing.Optional['__TwilioClient'] = None


def set_sms(twilio_account_sid: str, twilio_auth_token: str):
    global __twilio_singleton
    if __twilio_singleton:
        raise Exception
    __twilio_singleton = __TwilioClient(twilio_account_sid, twilio_auth_token)


def send(sender: str, receiver: str, body_template: str, template_data: dict):
    body = build_template(body_template, template_data)
    if get_setup().is_debug:
        logging.info('Not sending real sms in debug mode (activate with DEBUG=true environment variable)')
        logging.info('from:     %s', sender)
        logging.info('receiver: %s', receiver)
        logging.info('body:     %s', body)
        logging.info('done logging')
        return
    if not __twilio_singleton:
        raise OwnException(TWILIO_NOT_SETUP)
    __twilio_singleton.send_message(body, receiver, sender)


class __TwilioClient(object):
    def __init__(self, twilio_account_sid: str, twilio_auth_token: str):
        if twilio_account_sid and twilio_auth_token:
            self.twilio_client = Client(twilio_account_sid, twilio_auth_token)
        else:
            print("twilio not initialised (account sid and/or auth token is missing)")

    def send_message(self, body, receiver, sender):
        if self.twilio_client is None:
            raise OwnException(SMS_NOT_CONFIGURED)
        try:
            message = self.twilio_client.messages.create(
                body=body,
                to=receiver,
                from_=sender,
                # media_url=['https://demo.twilio.com/owl.png'])
            )
            logging.info('sending sms from: %s, receiver: %s, body: %s', sender, receiver, body)
        except TwilioRestException as e:
            raise OwnException(SMS_COULD_NOT_BE_SENT, e.msg)
