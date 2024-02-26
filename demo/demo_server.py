# py-scopes/demo/demo_server.py

from wsgiref.simple_server import make_server

def run(app, config):
    port = int(config.server_port)
    with make_server('', port, app) as httpd:
        print(f'Serving on port {port}.')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down.')


if __name__ == '__main__':
    import config
    run(config.app, config)
    #run(config.app_factory(), config)
    # see zope.app.wsgi.getWSGIApplication
