# py-scopes/demo/demo_server.py

from scopes.web.auth import oidc
from scopes.storage import topic

import logging
import waitress


def run(app, config):
    oidc.startup()  # todo: use generic app.startServices()
    port = int(config.server_port)
    print(f'Serving on port {port}.')
    waitress.serve(app, port=port)


if __name__ == '__main__':
    import config
    app = config.app_factory(config)
    run(app, config)
    # see zope.app.wsgi.getWSGIApplication
