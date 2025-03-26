# scopes.server.auth

from email.utils import formatdate
import json
from oic import oic, rndstr, unreserved
from oic.oic.message import AuthorizationResponse
import requests
from time import time
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

    def __init__(self, request):
        self.request = request
        self.params = config.oidc_params

    def authenticate(request):
        return None

    def login(self):
        req = self.request
        print('*** login', self, req.getTraversalStack(), req['PATH_INFO'])
        #print('***', dir(req))
        client = oic.Client()
        #providerInfo = client.provider_config(config.oidc_provider)
        #print('***', providerInfo)
        state = rndstr()
        nonce = rndstr()
        args = dict(
                client_id=self.params['client_id'],
                response_type='code', # 'code id_token token',
                state=state, nonce=nonce,
                scope=['openid', 'profile'],
                redirect_uri=self.params['callback_url'],
        )
        addArgs, codeVerifier = client.add_code_challenge()
        print('***', addArgs, codeVerifier)
        args.update(addArgs)
        self.storeSession(dict(state=state, nonce=nonce, code_verifier=codeVerifier))
        authReq = client.construct_AuthorizationRequest(request_args=args)
        loginUrl = authReq.request(self.params['auth_url'])
        print('***', loginUrl)
        req.response.redirect(loginUrl, trusted=True)

    def callback(self):
        req = self.request
        print('*** callback', self, req.form)
        data = self.loadSession()
        code = req.form['code']
        print('***', data, code)
        # !check state: req.form['state'] == data['state']
        args = dict(
                grant_type='authorization_code',
                code=code,
                redirect_uri=self.params['callback_url'],
                client_id=self.params['client_id'],
                code_verifier=data['code_verifier']
        )
        # !set header: 'Content-Type: application/x-www-form-urlencoded'
        tokenResponse = requests.post(self.params['token_url'], data=args)
        tdata =  tokenResponse.json()
        print('***', tdata)
        headers = dict(Authorization='Bearer ' + tdata['access_token'])
        userInfo = requests.get(self.params['userinfo_url'], headers=headers)
        print('***', userInfo.json())

    def storeSession(self, data):
        options = {}
        lifetime = int(self.params['cookie_lifetime'])
        options['expires'] = formatdate(time() + lifetime, localtime=False, usegmt=True)
        options['max-age'] = lifetime
        domain = self.params['cookie_domain']
        if domain:
            options['domain'] = domain
        #options['httponly'] = True
        name = self.params['cookie_name']
        value = json.dumps(data)
        self.request.response.setCookie(name, value, **options)

    def loadSession(self):
        cookie = self.request.getCookies().get(self.params['cookie_name'])
        if cookie is None:
            raise ValueError('Missing authentication cookie')
        data = json.loads(cookie)
        return data


@register('auth', Root)
def authView(context, request):
    print('*** auth', context, request['PATH_INFO'])
    return Authenticator(request)

@register('login', Authenticator)
def login(context, request):
    context.login()
    return DefaultView(context, request)

@register('callback', Authenticator)
def callback(context, request):
    context.callback()
    return DefaultView(context, request)

@register('logout', Authenticator)
def logout(context, request):
    print('*** logout', context, request['PATH_INFO'], request.getTraversalStack())
    return DefaultView(context, request)
