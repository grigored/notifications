import json
import logging
import traceback
import jsonschema
from http import HTTPStatus

from flask import request
from werkzeug.exceptions import BadRequest

from src.configs.exceptions import OwnException
from src.configs.strings import HANDLER_CRASHED, INVALID_JSON


def get_json(schema: dict):
    try:
        body = request.get_json(force=True)
    except ValueError as e:
        raise OwnException(INVALID_JSON)
    except BadRequest as e:
        raise OwnException(INVALID_JSON, data={'explanation': e.description})

    try:
        jsonschema.validate(body, schema)
        return body
    except (jsonschema.exceptions.ValidationError, jsonschema.exceptions.SchemaError) as e:
        raise OwnException(INVALID_JSON, data={'explanation': e.message})



def validate_request(schema=None):
    """
      Decorator needed for parameter matching against schema.
      :param dict schema:
    """

    def validate_request_decorator(handler):
        """
          Decorator that checks if the given json is valid and returns the object corresponding to that json.
          Will fail if the json format is invalid.
          Will fail if the json schema is wrong.
        """

        def check_request(self, *args, **kwargs):
            try:
                if schema is not None:
                    json_body = get_json(schema)
                    kwargs['received_json'] = json_body
                    logging.info('got request body: %s', json.dumps(json_body))
                return handler(self, *args, **kwargs)

            except OwnException as e:
                # error_stack = traceback.format_exc().splitlines()
                logging.error(traceback.format_exc())
                # catch all exceptions here and notify admin
                return self.send_failed(
                    e.message,
                    HTTPStatus.UNPROCESSABLE_ENTITY,
                    e.data
                )

            except:
                # error_stack = traceback.format_exc().splitlines()
                logging.error(traceback.format_exc())
                # catch all exceptions here and notify admin
                return self.send_failed(HANDLER_CRASHED, HTTPStatus.INTERNAL_SERVER_ERROR)

        return check_request

    return validate_request_decorator
