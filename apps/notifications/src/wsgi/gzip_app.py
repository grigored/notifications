import gzip
from io import BytesIO

from flask import request


class Gzip(object):

    def __init__(self, app, compress_level=6, minimum_response_length=500):
        self.app = app
        self.compress_level = compress_level
        self.minimum_response_length = minimum_response_length
        self.app.after_request(self.after_request)

    def after_request(self, response):
        accept_encoding = request.headers.get('Accept-Encoding', '').lower()
        if 'gzip' not in accept_encoding:
            return response

        if ((200 > response.status_code >= 300) or
                len(response.data) < self.minimum_response_length or
                'Content-Encoding' in response.headers):
            return response

        response.direct_passthrough = False

        gzip_buffer = BytesIO()
        gzip_file = gzip.GzipFile(mode='w', compresslevel=self.compress_level, fileobj=gzip_buffer)
        gzip_file.write(response.data)
        gzip_file.close()
        response.data = gzip_buffer.getvalue()
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Vary'] = 'Accept-Encoding'
        response.headers['Content-Length'] = len(response.data)

        return response
