import os
import typing

setup_singleton: typing.Optional['__Setup'] = None


def get_setup() -> '__Setup':
    if setup_singleton is None:
        raise Exception
    return setup_singleton


def set_setup(is_debug: bool):
    global setup_singleton
    if setup_singleton:
        raise Exception
    setup_singleton = __Setup(is_debug)


class S3Credentials(object):
    def __init__(self, api_key, api_secret, aws_region, default_bucket):
        self.api_key = api_key
        self.api_secret = api_secret
        self.aws_region = aws_region
        self.default_bucket = default_bucket


class __Setup(object):

    def __init__(self, is_debug: bool):
        self.is_debug = is_debug
        if not is_debug:
            self.s3_credentials = self.__get_s3_credentials()
        else:
            self.s3_credentials = self.__get_s3_credentials()
            self.s3_credentials.api_key = self.s3_credentials.api_key or 'AKIAJKXX4LWWHTFINZGA'
            self.s3_credentials.api_secret = self.s3_credentials.api_secret or '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'
            self.s3_credentials.aws_region = self.s3_credentials.aws_region or 'us-east-1'
            self.s3_credentials.default_bucket = self.s3_credentials.default_bucket or 'testbucket'

    def __get_s3_credentials(self) -> S3Credentials:
        return S3Credentials(
            os.environ.get('AWS_S3_API_KEY'),
            os.environ.get('AWS_S3_API_SECRET'),
            os.environ.get('AWS_S3_REGION'),
            os.environ.get('DEFAULT_BUCKET'),
        )
