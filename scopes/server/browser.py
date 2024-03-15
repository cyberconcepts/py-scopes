# scopes.server.browser

import json
from zope.interface import implementer
from scopes.interfaces import IContainer, IReference, IView

views = {} # registry for all views: {name: {prefix: viewClass, ...}, ...}

def register(name, *contextClasses):
    """Use as decorator: `@register(name, class, ...). 
       class `None` means default view for all classes."""
    def doRegister(viewClass):
        nameEntry = views.setdefault(name, {})
        for cl in contextClasses:
            key = cl and cl.prefix or ''
            nameEntry[key] = viewClass
        return viewClass
    return doRegister

def getView(request, ob, name):
    nameEntry = views.get(name)
    if nameEntry is None:
        return None
    viewClass = nameEntry.get(ob.__class__.prefix)
    if viewClass is None:
        viewClass = nameEntry.get('')
    if viewClass is None:
        return None
    return viewClass(ob, request)


@register('index.html', None)
@register('index.json', None)
@implementer(IView)
class DefaultView:

    def __init__(self, context, request):
        self.context = context
        self.request = request

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
        return result

    def renderJson(self, result):
        self.request.response.setHeader('Content-type', 'application/json; charset=utf-8')
        return json.dumps(result).encode('UTF-8')

    def __call__(self):
        result = self.prepareResult()
        return self.renderJson(result)

