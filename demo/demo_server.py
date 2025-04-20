# py-scopes/demo/demo_server.py

from scopes.web.auth import oidc
from scopes.storage import topic

import logging
import waitress
from wsgiref.simple_server import make_server


def run(app, config):
    port = int(config.server_port)
    print(f'Serving on port {port}.')
    waitress.serve(app, port=port)


if __name__ == '__main__':
    import config
    app = config.app_factory(config)
    run(app, config)
    # see zope.app.wsgi.getWSGIApplication
