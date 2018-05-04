from http import HTTPStatus

from flask import make_response
from flask.views import MethodView


class HealthCheckHandler(MethodView):
    def get(self):
        response = make_response('OK', HTTPStatus.OK.value)
        return response
