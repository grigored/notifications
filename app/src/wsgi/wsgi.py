#!/usr/bin/python
from src.setup import set_setup
from src.wsgi.backend_routes import configure_app
import os

debug = os.environ.get('DEBUG') == "true"

set_setup(debug)
app = configure_app(debug)

if debug:
    print('running in debug mode')
    app.run(host="0.0.0.0", debug=debug, port=8001, threaded=True)
else:
    print('running in production mode')
    app = configure_app(debug)
