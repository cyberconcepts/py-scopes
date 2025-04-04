# scopes.server.auth

from cryptography.fernet import Fernet
from email.utils import formatdate
import json
import requests
from time import time
from urllib.parse import urlencode
from zope.authentication.interfaces import IAuthentication
from zope.interface import implementer
from zope.publisher.interfaces import Unauthorized

from scopes.server.browser import DefaultView, register
from scopes.storage.folder import DummyFolder, Root
from scopes import util

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
        self.reqUrl = config.base_url
        self.setCrypt(self.params['cookie_crypt'])

    def setReqUrl(self, base, path):
        self.reqUrl = '/'.join((base, path))

    def setCrypt(self, key):
        self.cookieCrypt = key and Fernet(key.encode('ASCII')) or None

    def authenticate(request):
        ''' return user data or None '''
        return None

    def login(self):
        req = self.request
        print('*** login', self, req.getTraversalStack(), req['PATH_INFO'])
        #print('***', dir(req))
        state = util.rndstr()
        nonce = util.rndstr()
        codeVerifier = util.rndstr2()
        codeChallenge = util.hashS256(codeVerifier)
        args = dict(
                client_id=self.params['client_id'],
                response_type='code', # 'code id_token token',
                state=state, nonce=nonce,
                code_challenge=codeChallenge, code_challenge_method='S256',
                scope='openid profile email urn:zitadel:iam:user:resourceowner',
                redirect_uri=self.params['callback_url'],
                request_uri=self.reqUrl,
        )
        self.storeSession(dict(state=state, nonce=nonce, code_verifier=codeVerifier))
        loginUrl = '?'.join((self.params['auth_url'], urlencode(args)))
        print('***', loginUrl)
        req.response.redirect(loginUrl, trusted=True)

    def callback(self):
        req = self.request
        print('*** callback', self, req.form)
        sdata = self.loadSession()
        code = req.form['code']
        print('*** session data', sdata, code)
        # !check state: req.form['state'] == sdata['state']
        args = dict(
                grant_type='authorization_code',
                code=code,
                redirect_uri=self.params['callback_url'],
                client_id=self.params['client_id'],
                code_verifier=sdata['code_verifier']
        )
        # !set header: 'Content-Type: application/x-www-form-urlencoded'
        tokenResponse = requests.post(self.params['token_url'], data=args)
        tdata =  tokenResponse.json()
        print('*** token response', tdata)
        headers = dict(Authorization='Bearer ' + tdata['access_token'])
        userInfo = requests.get(self.params['userinfo_url'], headers=headers)
        print('***', userInfo.json())
        # get relevant data from userInfo
        # set up session data for authenticate()
        ndata = dict(
        )
        self.storeSession(ndata)
        req.response.redirect(self.reqUrl, trusted=True)

    def logout(self):
        pass

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
        if self.cookieCrypt:
            value = self.cookieCrypt.encrypt(value.encode('ASCII')).decode('ASCII')
        self.request.response.setCookie(name, value, **options)

    def loadSession(self):
        cookie = self.request.getCookies().get(self.params['cookie_name'])
        if cookie is None:
            raise ValueError('Missing authentication cookie')
        if self.cookieCrypt:
            cookie = self.cookieCrypt.decrypt(cookie).decode('ASCII')
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
