import uuid
from io import StringIO

import boto
import boto3
from boto.s3.key import Key
from botocore.config import Config

from src.configs.exceptions import OwnException
from src.configs.strings import MISSING_BUCKET_NAME, MISSING_BUCKET_REGION, NO_FILE_SPECIFIED, UNKNOWN_FILE
from src.setup import get_setup

TEN_MB = (1024 ** 2) * 10


def upload_from_server(data_file, upload_file_name, bucket_name=None, public=False, content_type=None):
    """

    @param data_file: the file that you want to upload
    @param upload_file_name: the file path where to upload, eg: upload_folder/file_name.txt, or file_name.jpg
    @param public: visibility of file on S3

    @return: the url of the uploaded file
    """

    if data_file is None:
        raise OwnException(NO_FILE_SPECIFIED)

    conn = boto.connect_s3()
    # conn = boto.s3.connect_to_region(region_name='the_region')
    # conn = S3Connection('aws_key', 'aws_secret')
    bucket_name = __get_bucket_name(bucket_name)
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    k.key = upload_file_name
    policy = 'public-read' if public else 'private'
    k.content_type = content_type
    k.set_contents_from_file(data_file, policy=policy)
    # k.set_contents_from_string(data_file, policy=policy)

    url = k.generate_url(expires_in=0, query_auth=False)

    return url


def upload_string_from_server(string_value, upload_file_name, bucket_name=None, public=False, is_pdf=True):
    conn = boto.connect_s3()
    # conn = boto.s3.connect_to_region(region_name='the_region')
    # conn = S3Connection('aws_key', 'aws_secret')
    bucket_name = __get_bucket_name(bucket_name)
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    k.key = upload_file_name
    k.content_type = 'application/pdf' if is_pdf else ''
    policy = 'public-read' if public else 'private'
    k.set_contents_from_string(string_value, policy=policy)


def download_string_from_s3(upload_file_name, bucket_name=None):
    conn = boto.connect_s3()
    # conn = boto.s3.connect_to_region(region_name='the_region')
    # conn = S3Connection('aws_key', 'aws_secret')
    bucket_name = __get_bucket_name(bucket_name)
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    k.key = upload_file_name
    downloaded_file = StringIO()
    k.get_contents_to_file(downloaded_file)
    downloaded_file.seek(0)
    return downloaded_file


def get_data_for_s3_post(bucket_name=None, bucket_region=None, upload_file_name=None, upload_file_type="",
                         public=False, max_file_size=TEN_MB, post_expire_in=3600):
    """

    @param bucket_name: bucket name
    @param upload_file_name: the file path where to upload, eg: upload_folder/file_name.txt, or file_name.jpg; if no
    file name is provided, it will use by default uuid.uuid4()
    @param upload_file_type: type of the to-be-uploaded file, eg: image/, application/pdf
    @param public: visibility of file on S3
    (more here http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUTacl.html)
    @param max_file_size: the max file size that S3 should accept (in bytes)
    @param post_expire_in: the number of seconds the presigned post is valid for

    @return: a dict containing the information needed for the client to do the POST request
    """
    if upload_file_name is None or upload_file_name == '':
        # raise UploadFileException(EMPTY_FILE_NAME)
        upload_file_name = str(uuid.uuid4())

    bucket_name = __get_bucket_name(bucket_name)
    bucket_region = bucket_region or get_setup().s3_credentials.aws_region
    if not bucket_region:
        raise OwnException(MISSING_BUCKET_REGION)
    key = upload_file_name
    s3 = boto3.client(
        's3',
        region_name=bucket_region,
        config=Config(signature_version='s3v4'),
    )
    # conn = boto.connect_s3()
    # conn.build_post_policy(time() + 1000, {})
    policy = 'public-read' if public else 'private'
    post_data = s3.generate_presigned_post(
        Bucket=bucket_name,
        Key=key,
        Fields={'acl': policy},
        Conditions=[
            {'acl': policy},
            ['content-length-range', 0, max_file_size],
            ["starts-with", "$Content-Type", upload_file_type or 'image/'],
        ],
        ExpiresIn=post_expire_in
    )

    fields = post_data.get('fields')
    fields['bucket'] = bucket_name
    fields['Content-Type'] = upload_file_type or 'image/jpeg'

    return fields


def get_url_for_private_file(key, bucket_name=None):
    """
    More information here: http://www.gyford.com/phil/writing/2012/09/26/django-s3-temporary.php
    @return:
    """
    conn = boto.connect_s3()
    # conn = boto.s3.connect_to_region(region_name='the_region')
    # conn = S3Connection('aws_key', 'aws_secret')
    bucket_name = __get_bucket_name(bucket_name)
    s3_key = conn.get_bucket(bucket_name).get_key(key)

    if s3_key is None:
        raise OwnException(UNKNOWN_FILE)

    return s3_key.generate_url(60, 'GET', force_http=True)


def __get_bucket_name(bucket_name=None):
    bucket_name = bucket_name or get_setup().s3_credentials.default_bucket
    if not bucket_name:
        raise OwnException(MISSING_BUCKET_NAME)
    return bucket_name
