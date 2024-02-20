# py-scopes/demo/server.py

from wsgiref.simple_server import make_server

def run(app, config):
    port = int(config.server_port)
    with make_server('', port, app) as httpd:
        print(f'Serving on port {port}.')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down.')
