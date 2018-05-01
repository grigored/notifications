import traceback

import requests
from flask import make_response
from flask.views import MethodView
from http import HTTPStatus


class HealthCheckHandler(MethodView):
    def get(self):
        jobs_url = 'http://jobs:8001/'
        try:
            response = requests.get(jobs_url)
            success = True
            stack_trace = None
        except:
            response = None
            success = False
            stack_trace = traceback.format_exc()

        if not success or not response or response.status_code != HTTPStatus.OK.value:
            pass

        response = make_response('OK', HTTPStatus.OK.value)
        return response
