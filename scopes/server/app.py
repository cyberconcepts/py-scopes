# scopes.server.app

from zope.publisher.base import DefaultPublication
from zope.publisher.browser import BrowserRequest
from zope.publisher.interfaces import NotFound
from zope.publisher.publish import publish

from scopes.interfaces import ITraversable, IView
from scopes.server.browser import getView
from scopes.storage.folder import Root


def zope_app_factory(config):
    storageFactory = config.StorageFactory(config)
    def zope_app(environ, start_response):
        storage = storageFactory(config.dbschema)
        appRoot = Root(storage, config)
        request = BrowserRequest(environ['wsgi.input'], environ)
        request.setPublication(Publication(appRoot))
        request = publish(request, False)
        response = request.response
        start_response(response.getStatusString(), response.getHeaders())
        return response.consumeBodyIter()
    return zope_app


class Publication(DefaultPublication):

    def traverseName(self, request, ob, name):
        next = getView(request, ob, name)
        if next is not None:
            return next
        if ITraversable.providedBy(ob):
            next = ob.get(name)
        if next is None:
            raise NotFound(ob, name, request)
        return next

    def getDefaultTraversal(self, request, ob):
        if IView.providedBy(ob):
            return ob, ()
        return ob, ('index.html',)

