import logging
import typing
import os


setup_singleton: typing.Optional['__Setup'] = None


def get_setup() -> '__Setup':
    if setup_singleton is None:
        raise Exception
    return setup_singleton


def set_setup(is_debug: bool):
    global setup_singleton
    if setup_singleton:
        raise Exception
    logging.basicConfig(level=logging.INFO)
    setup_singleton = __Setup(is_debug)


class EmailCredentials(object):
    def __init__(self, api_key, api_secret, aws_region, email_sender):
        self.api_key = api_key
        self.api_secret = api_secret
        self.aws_region = aws_region
        self.email_sender = email_sender


class SmsCredentials(object):
    def __init__(self, sid, token, phone_number):
        self.sid = sid
        self.token = token
        self.phone_number = phone_number


class __Setup(object):

    def __init__(self, is_debug: bool):
        self.is_debug = is_debug
        if not is_debug:
            self.email_credentials = self.__get_email_credentials()
            self.sms_credentials = self.__get_sms_credentials()
        else:
            self.email_credentials = EmailCredentials("", "", "", "grigore@instacarshare.com")
            self.sms_credentials = SmsCredentials("", "", "")

    def __get_email_credentials(self) -> EmailCredentials:
        return EmailCredentials(
            os.environ.get('AWS_EMAIL_API_KEY'),
            os.environ.get('AWS_EMAIL_API_SECRET'),
            os.environ.get('AWS_EMAIL_REGION'),
            os.environ.get('EMAIL_SENDER'),
        )

    def __get_sms_credentials(self) -> SmsCredentials:
        return SmsCredentials(
            os.environ.get('TWILIO_ACCOUNT_SID'),
            os.environ.get('TWILIO_TOKEN'),
            os.environ.get('SMS_SENDER'),
        )
