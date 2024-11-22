# scopes.server.auth

from zope.authentication.interfaces import IAuthentication
from zope.interface import implementer
from zope.publisher.interfaces import Unauthorized


def authenticate(request):
    #print('*** authenticate')
    return None


@implementer(IAuthentication)
class JwtAuthentication:

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

