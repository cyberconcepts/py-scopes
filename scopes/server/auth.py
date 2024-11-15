# scopes.server.auth

from zope.authentication.interfaces import IAuthentication
from zope.principalregistry.principalregistry import PrincipalRegistry
from zope.component import getUtility, provideUtility, queryNextUtility
from zope.interface import implementer

baseAuth = None

class JwtAuthentication(PrincipalRegistry):

    def authenticate(self, request):
        prc = authenticate(request)
        if prc is None:
            return baseAuth.authenticate(request)

    def getPrincipal(self, id):
        return baseAuth.getPrincipal(id)

    def unauthenticatedPrincipal(self):
        return baseAuth.unauthenticatedPrincipal()

    def unauthorized(self, id, request):
        return baseAuth.unauthorized(id, request)



def authenticate(request):
    print('*** authenticate')
    return None


def registerAuthUtility():
    global baseAuth
    baseAuth = getUtility(IAuthentication)
    print('*** registerAuthUtility, baseAuth:', baseAuth)
    provideUtility(JwtAuthentication(), IAuthentication)
    
