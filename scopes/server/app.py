# scopes.server.app

from zope.publisher.base import DefaultPublication
from zope.publisher.browser import BrowserRequest
from zope.publisher.publish import publish
from zope.traversing.publicationtraverse import PublicationTraverser

from scopes.storage.folder import Root


def zope_app_factory(config):
    storageFactory = config.StorageFactory(config)
    def zope_app(environ, start_response):
        storage = storageFactory(config.dbschema)
        appRoot = Root(storage, config)
        request = BrowserRequest(environ['wsgi.input'], environ)
        request.setPublication(Publication(appRoot))
        request = publish(request, True)
        response = request.response
        start_response(response.getStatusString(), response.getHeaders())
        return response.consumeBodyIter()
    return zope_app


class Publication(DefaultPublication):

    pass

