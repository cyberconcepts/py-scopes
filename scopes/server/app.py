# scopes.server.app

import json
from zope.interface import implementer
from zope.publisher.base import DefaultPublication
from zope.publisher.browser import BrowserRequest
from zope.publisher.interfaces import NotFound
from zope.publisher.publish import publish
from zope.traversing.publicationtraverse import PublicationTraverser

from scopes.interfaces import IContainer, ITraversable, IView
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
        next = None
        if ITraversable.providedBy(ob):
            next = ob.get(name)
        if next is None:
            if name == 'index.html':
                next = DefaultView(ob, request)
        if next is None:
            raise NotFound(ob, name, request)
        return next

    def getDefaultTraversal(self, request, ob):
        if IView.providedBy(ob):
            return ob, ()
        return ob, ('index.html',)


@implementer(IView)
class DefaultView:

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        ob = self.context
        result = dict(head=ob.head, data=ob.data)
        if IContainer.providedBy(ob):
            result['items'] = list(ob.keys())
        return json.dumps(result)

