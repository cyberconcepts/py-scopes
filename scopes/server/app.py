# scopes.server.app

from zope.publisher.base import DefaultPublication
from zope.publisher.browser import BrowserRequest
from zope.publisher.publish import publish
from zope.traversing.publicationtraverse import PublicationTraverser

from scopes.storage.folder import Root


def demo_app(environ, start_response):
    print(f'*** environ {environ}.')
    status = '200 OK'
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return ['Hello World'.encode()]


def zope_app_factory(config):
    config.storageFactory = config.StorageFactory(config)
    def zope_app(environ, start_response):
        request = BrowserRequest(environ['wsgi.input'], environ)
        storage = config.storageFactory(config.dbschema)
        appRoot = Root(storage, config)
        request.setPublication(DefaultPublication(appRoot))
        request = publish(request, False)
        response = request.response
        start_response(response.getStatusString(), response.getHeaders())
        return response.consumeBodyIter()
    return zope_app


class AppRoot:
    """Zope Demo AppRoot"""

    def __init__(self, config):
        self.config = config

    def __call__(self):
        """calling AppRoot"""
        return 'At root'

    def __getitem__(self, key):
        def child():
            """get child"""
            print(f'--- getitem {key}')
            return 'getitem'
        return child

    def hello(self): 
        """method hello"""
        return 'Hello AppRoot'


