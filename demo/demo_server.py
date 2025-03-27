# py-scopes/demo/demo_server.py

from scopes.server import auth
from scopes.storage import topic

import waitress
from wsgiref.simple_server import make_server

def run(app, config):
    port = int(config.server_port)
    print(f'Serving on port {port}.')
    waitress.serve(app, port=port)

def run_wsgiref(app, config):   # obsolete
    with make_server('', port, app) as httpd:
        print(f'Serving on port {port}.')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down.')


if __name__ == '__main__':
    import config
    app = config.app_factory(config)
    run(app, config)
    # see zope.app.wsgi.getWSGIApplication
