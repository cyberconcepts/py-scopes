# scopes.server.auth

from zope.authentication.interfaces import IAuthentication
from zope.interface import implementer
from zope.publisher.interfaces import Unauthorized

from scopes.server.browser import DefaultView, register
from scopes.storage.folder import DummyFolder, Root


def authenticate(request):
    #print('*** authenticate')
    return None


@implementer(IAuthentication)
class OidcAuthentication:

    def __init__(self, baseAuth):
        self.baseAuth = baseAuth

    def authenticate(self, request):
        prc = authenticate(request)
        if prc is None and self.baseAuth is not None:
            prc = self.baseAuth.authenticate(request)
        return prc

    def getPrincipal(self, id):
        if self.baseAuth is not None:
            return self.baseAuth.getPrincipal(id)

    def unauthenticatedPrincipal(self):
        if self.baseAuth is not None:
            return self.baseAuth.unauthenticatedPrincipal()

    def unauthorized(self, id, request):
        if self.baseAuth is not None:
            return self.baseAuth.unauthorized(id, request)

    def logout(self, request):
        print('*** JwtAuthentication: logout')

JwtAuthentication = OidcAuthentication  # old name - still used?


class Authenticator(DummyFolder):
    prefix = 'auth'


@register('auth', Root)
def authView(context, request):
    print('*** auth', context, request['PATH_INFO'], request.getTraversalStack())
    return Authenticator()

@register('login', Authenticator)
def login(context, request):
    print('*** login', context, request['PATH_INFO'], request.getTraversalStack())
    return DefaultView(context, request)
