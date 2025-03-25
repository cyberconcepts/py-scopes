# scopes.server.auth

from oic import oic, rndstr
from oic.oic.message import AuthorizationResponse

from zope.authentication.interfaces import IAuthentication
from zope.interface import implementer
from zope.publisher.interfaces import Unauthorized

from scopes.server.browser import DefaultView, register
from scopes.storage.folder import DummyFolder, Root

import config


def authenticate(request):
    #print('*** authenticate')
    return None


@implementer(IAuthentication)
class OidcAuthentication:

    def __init__(self, baseAuth):
        self.baseAuth = baseAuth

    def authenticate(self, request):
        prc = authenticate(request)
        # prc = Authenticator().authenticate(request)
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
        print('*** OidcAuthentication: logout')

JwtAuthentication = OidcAuthentication  # old name - still used?


class Authenticator(DummyFolder):

    prefix = 'auth'

    def authenticate(request):
        return None

    def login(self, request):
        params = config.oidc_params
        print('*** login', self, request.getTraversalStack(), request['PATH_INFO'])
        #print('***', dir(request))
        client = oic.Client()
        #providerInfo = client.provider_config(params['provider_url'])
        #print('***', providerInfo)
        #client.register(providerInfo['registration_endpoint'], application_type='web')
        requestArgs = dict(
                client_id=params['client_id'],
                response_type='code', # 'code id_token token',
                state=rndstr(), nonce=rndstr(),
                scope=['openid', 'profile'],
                redirect_uri=params['callback_url'],
        )
        authReq = client.construct_AuthorizationRequest(request_args=requestArgs)
        #loginUrl = authReq.request(client.authorization_endpoint)
        loginUrl = authReq.request(params['provider_url'])
        print('***', loginUrl)
        request.response.redirect(loginUrl, trusted=True)

    def callback(self, request):
        print('*** callback', self, request.form)
        code = request.form['code']


@register('auth', Root)
def authView(context, request):
    print('*** auth', context, request['PATH_INFO'])
    return Authenticator()

@register('login', Authenticator)
def login(context, request):
    context.login(request)
    return DefaultView(context, request)

@register('callback', Authenticator)
def callback(context, request):
    context.callback(request)
    return DefaultView(context, request)

@register('logout', Authenticator)
def logout(context, request):
    print('*** logout', context, request['PATH_INFO'], request.getTraversalStack())
    return DefaultView(context, request)
