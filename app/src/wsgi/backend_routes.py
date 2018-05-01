#!/usr/bin/python
import socket

from flask import Flask
from raven import Client
from raven.contrib.flask import Sentry
from werkzeug.contrib.fixers import ProxyFix

from src.configs.sentry_conf import set_sentry, SENTRY_LIST_MAX_LENGTH, SENTRY_STRING_MAX_LENGTH
from src.wsgi.gzip_app import Gzip
from src.handlers import (
    health_check_handler,
    send_notification_handler,
)


def add_routes(app):
    base_regex = '/api/%s/'
    routes_base_v1 = {
        'send-notification': send_notification_handler.SendNotificationHandler,
    }

    # routes_base_v1_3 = {route: handler for route, handler in routes_base_v1_2.items()}
    # routes_base_v1_3.update({
    #     'reserve': reserve_handler.ReserveApiHandler,
    # })

    routes_base = [
        {'version': 'v1', 'routes': routes_base_v1},
        # {'version': 'v1.3', 'routes': routes_base_v1_3},
    ]
    for base_route in routes_base:
        for route, handler in base_route['routes'].items():
            url = base_regex % base_route['version'] + route
            view_title = '%s/%s' % (base_route['version'], route)
            app.add_url_rule(url, view_func=handler.as_view(view_title))

    app.add_url_rule('/health-check', view_func=health_check_handler.HealthCheckHandler.as_view('health-check'))


def get_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


def configure_app(debug):
    app = Flask(__name__)
    if not debug:
        set_sentry(Sentry(
            app,
            client=Client(
                'https://f994ce7d7cd94917824c97879b551079:7d12f8f9a99545988e1c4ae80ab7fc60@sentry.io/170411',
                list_max_length=SENTRY_LIST_MAX_LENGTH,
                string_max_length=SENTRY_STRING_MAX_LENGTH,
            )
        ))
        gzip = Gzip(app)
        app = gzip.app
        app.wsgi_app = ProxyFix(app.wsgi_app)
    add_routes(app)
    return app
