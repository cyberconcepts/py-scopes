# scopes.server.app

from zope.publisher.base import DefaultPublication
from zope.publisher.browser import BrowserRequest
from zope.publisher.publish import publish
from zope.traversing.publicationtraverse import PublicationTraverser


def demo_app(environ, start_response):
    print(f'*** environ {environ}.')
    status = '200 OK'
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    return ['Hello World'.encode()]


def zope_app(environ, start_response):
    request = BrowserRequest(environ['wsgi.input'], environ)
    request.setPublication(DefaultPublication(AppRoot()))
    request = publish(request, False)
    response = request.response
    start_response(response.getStatusString(), response.getHeaders())
    return response.consumeBodyIter()


class AppRoot:
    """Zope Demo AppRoot"""

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


