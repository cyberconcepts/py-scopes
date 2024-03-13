# scopes.server.browser

import json
from zope.interface import implementer
from scopes.interfaces import IContainer, IView

views = {}

def register(contextClass, name):
    def doRegister(viewClass):
        nameEntry = views.setdefault(name, {})
        key = contextClass and contextClass.prefix or ''
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


@register(None, 'index.html')
@register(None, 'index.json')
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
        print('***', result)
        return json.dumps(result)

