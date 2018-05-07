import json
from http import HTTPStatus

from flask import make_response, request
from flask.views import MethodView


class BaseApiHandler(MethodView):

    def get_query_arg(self, query_name):
        return request.args.get(query_name, default=None)

    def __get_response_headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
        }

    def __send(self, ret: dict, code, pdf_name):

        code_value = int(code)

        if pdf_name is None:
            ret = json.dumps(ret)

        response = make_response(ret, code_value)
        response.headers = self.__get_response_headers()

        if pdf_name is not None:
            response.headers['Content-Disposition'] = 'inline; filename=%s' % pdf_name
            response.headers['Content-Type'] = 'application/pdf'

        return response

    def send_pdf(self, pdf_string, pdf_name):
        return self.__send(pdf_string, HTTPStatus.OK, pdf_name)

    def send_failed(
            self,
            error_message: str,
            error_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            error_details: dict = None
    ):
        if error_details is not None:
            error_details.update({'error': error_message})
        else:
            error_details = {'error': error_message}
        return self.__send(error_details, error_code, None)

    def send_success(
            self,
            message: dict,
            http_code=HTTPStatus.OK,
            file_type=None
    ):
        return self.__send(message, http_code, file_type)
