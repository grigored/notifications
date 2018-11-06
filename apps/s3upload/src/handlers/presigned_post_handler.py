from src.handlers.http_decorators import validate_request

from src.configs.exceptions import OwnException
from src.handlers.base_api_handler import BaseApiHandler
from src.handlers.handlers_schemas import schema_get_data
from src.upload.upload import TEN_MB, get_data_for_s3_post


class Handler(BaseApiHandler):
    @validate_request(schema_get_data)
    def post(self, received_json):
        try:
            data = get_data_for_s3_post(
                bucket_name=received_json.get('bucket'),
                bucket_region=received_json.get('bucketRegion'),
                upload_file_name=received_json.get('filename'),
                upload_file_type=received_json.get('filetype'),
                public=received_json.get('public'),
                max_file_size=received_json.get('maxFileSize') or TEN_MB,
                post_expire_in=received_json.get('postExpire') or 3600,
            )
        except OwnException as e:
            return self.send_failed(e.message)

        return self.send_success(data)
