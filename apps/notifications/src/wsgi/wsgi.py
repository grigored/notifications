#!/usr/bin/python
import logging
import sys

from src.notifications.sms import set_sms
from src.setup import set_setup, get_setup
from src.wsgi.backend_routes import configure_app
import os

logging.basicConfig(level=logging.INFO)

debug = os.environ.get('DEBUG') == "true"
production = os.environ.get('PRODUCTION') == "true"
port = os.environ.get('PORT')

if production:
    print('running in production mode')

    if port == "":
        logging.info('Port is missing. Use the "PORT" environment variable to set it')
        sys.exit(-1)
    try:
        port = int(port)
    except:
        logging.info('Port is not int. Use the "PORT" environment variable to set it')
        sys.exit(-1)

    set_setup(False)
    set_sms(get_setup().sms_credentials.sid, get_setup().sms_credentials.token)
    app = configure_app(False)
else:
    print('running in debug mode')
    set_setup(debug)
    if not debug:
        set_sms(get_setup().sms_credentials.sid, get_setup().sms_credentials.token)
    app = configure_app(debug)
    app.run(host="0.0.0.0", debug=True, port=8006, threaded=True)
