#!/usr/bin/python
import logging

from src.setup import set_setup, get_setup
from src.wsgi.backend_routes import configure_app
import os
import sys

logging.basicConfig(level=logging.INFO)
production = os.environ.get('PRODUCTION') == "true"
port = os.environ.get('PORT')

if port == "":
    logging.info('Port is missing. Use the "PORT" environment variable to set it')
    sys.exit(-1)
try:
    port = int(port)
except:
    logging.info('Port is not int. Use the "PORT" environment variable to set it')
    sys.exit(-1)

if production:
    print('running in production mode')
    set_setup(False)
    app = configure_app(False)
else:
    print('running in debug mode')
    set_setup(True)
    app = configure_app(True)
    app.run(host="0.0.0.0", debug=True, port=port, threaded=True)
