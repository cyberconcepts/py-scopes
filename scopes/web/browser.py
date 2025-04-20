# scopes.web.browser

import json
import logging
from zope.interface import implementer
from scopes.interfaces import IContainer, IReference, IView

logger = logging.getLogger('web.browser')

views = {} # registry for all views: {name: {prefix: viewClass, ...}, ...}

def register(name, *contextTypes):
    """Use as decorator: `@register(name, class_or_prefix, ...). 
       No class (or `None` or `''`) means default view for all classes."""
    def doRegister(factory):
        implementer(IView)(factory)
        nameEntry = views.setdefault(name, {})
        cts = contextTypes or ['']
        for ct in cts:
            if not isinstance(ct, str):
                ct = ct.prefix
            nameEntry[ct] = factory
        return factory
    return doRegister

def getView(request, ob, name):
    nameEntry = views.get(name)
    if nameEntry is None:
        return None
    factory = nameEntry.get(ob.prefix)
    if factory is None:
        factory = nameEntry.get('')
    if factory is None:
        return None
    logger.debug('getView: %s %s', ob, request['PATH_INFO'])
    return factory(ob, request)


@register('index.html')
@register('index.json')
class DefaultView:

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        result = self.prepareResult()
        return self.render(result)

    def prepareResult(self):
        ob = self.context
        result = ob.asDict()
        if IContainer.providedBy(ob):
            result['items'] = [v.asDict() for v in ob.values()]
        if IReference.providedBy(ob):
            target = ob.getTarget()
            if target:
                result['target'] = target.asDict()
                if IContainer.providedBy(target):
                    result['target']['items'] = [v.asDict() for v in target.values()]
        prc = self.request.principal
        if prc is not None:
            result['principal'] = prc.asDict()
        return result

    def render(self, result):
        self.request.response.setHeader('Content-type', 'application/json; charset=utf-8')
        return json.dumps(result).encode('UTF-8')
