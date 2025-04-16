# scopes.server.app

import logging
from zope.i18n.interfaces import IUserPreferredCharsets
from zope.interface import implementer
from zope.publisher.base import DefaultPublication
from zope.publisher.browser import BrowserRequest
from zope.publisher.interfaces import NotFound
from zope.publisher.publish import publish

from scopes.interfaces import ITraversable, IView
from scopes.server.browser import getView
import scopes.storage.concept # register container classes
from scopes.storage.folder import Root


@implementer(IUserPreferredCharsets)
class Request(BrowserRequest):
    def getPreferredCharsets(self):
        return ['UTF-8']


def zope_app_factory(config):
    storageFactory = config.StorageFactory(config)
    def zope_app(environ, start_response):
        storage = storageFactory(config.dbschema)
        appRoot = Root(storage)
        request = Request(environ['wsgi.input'], environ)
        request.setPublication(Publication(appRoot))
        request = publish(request, True)
        response = request.response
        start_response(response.getStatusString(), response.getHeaders())
        return response.consumeBodyIter()
    return zope_app


class Publication(DefaultPublication):

    def beforeTraversal(self, request):
        super(Publication, self).beforeTraversal(request)
        from scopes.server.auth import authentication
        prc = authentication.authenticate(request)
        request.setPrincipal(prc)

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

    def handleException(self, ob, request, exc_info, retry_allowed=True):
        if exc_info[0] != NotFound:
            raise
        request.response.reset()
        request.response.handleException(exc_info)

