#!/usr/bin/python
from src.setup import set_setup
from src.wsgi.backend_routes import configure_app
import os

debug = os.environ.get('DEBUG') == "true"
production = os.environ.get('PRODUCTION') == "true"


if production:
    print('running in production mode')
    set_setup(False)
    app = configure_app(False)
else:
    print('running in debug mode')
    set_setup(debug)
    app = configure_app(debug)
    app.run(host="0.0.0.0", debug=True, port=8001, threaded=True)
