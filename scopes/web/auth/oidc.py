# scopes.web.auth.uidc

from cryptography.fernet import Fernet
from email.utils import formatdate
import json
import logging
import requests
from time import time
from urllib.parse import urlencode
from zope.authentication.interfaces import IAuthentication, IPrincipal
from zope.interface import implementer
from zope.publisher.interfaces import Unauthorized
from zope.security.interfaces import IGroupAwarePrincipal

from scopes.web.browser import DefaultView, register
from scopes.storage.folder import DummyFolder, Root
from scopes import util

import config

logger = logging.getLogger('web.auth.oidc')


@implementer(IAuthentication)
class OidcAuthentication:

    def __init__(self, baseAuth):
        self.baseAuth = baseAuth

    def authenticate(self, request):
        auth = Authenticator(request)
        prc = auth.authenticate()
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
        Authenticator(request).login()

    def logout(self, request):
        Authenticator(request).logout()

authentication = OidcAuthentication(None)


@implementer(IGroupAwarePrincipal)
class Principal:

    group_prefix = 'gloops.'

    def __init__(self, id, data):
        self.id = id
        self.data = data

    @property
    def title(self):
        return self.data['name']

    @property
    def groups(self):
        groups = [self.group_prefix + g for g in self.data.get('groups', [])]
        return groups

    def asDict(self):
        data = self.data.copy()
        data['id'] = self.id
        return data


class Authenticator(DummyFolder):

    prefix = 'auth.oidc'

    oidcProviderUris = ['authorization_endpoint', 'token_endpoint', 
                        'introspection_endpoint', 'userinfo_endpoint',
                        'revocation_endpoint', 'end_session_endpoint',
                        'device_authorization_endpoint', 'jwks_uri']

    def __init__(self, request):
        self.request = request
        self.params = config.oidc_params
        self.reqUrl = config.base_url
        self.setCrypt(self.params.get('cookie_crypt'))
        self.loadOidcProviderData()

    def setReqUrl(self, base, path):
        self.reqUrl = '/'.join((base, path))

    def setCrypt(self, key):
        self.cookieCrypt = key and Fernet(key) or None

    def authenticate(self):
        ''' return  principal or None'''
        data = self.loadSession()
        logger.debug('authenticate: %s', data)
        if data and 'userid' in data:
            id = self.params.get('principal_prefix', '') + data.pop('userid')
            return Principal(id, data)
        return None

    def login(self):
        req = self.request
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
        authUrl = self.params['op_uris']['authorization_endpoint']
        loginUrl = '?'.join((authUrl, urlencode(args)))
        logger.debug('login: URL %s', loginUrl)
        req.response.redirect(loginUrl, trusted=True)

    def callback(self):
        req = self.request
        logger.debug('callback: %s %s', self, req.form)
        sdata = self.loadSession()
        code = req.form['code']
        # !check state: req.form['state'] == sdata['state']
        args = dict(
                grant_type='authorization_code',
                code=code,
                redirect_uri=self.params['callback_url'],
                client_id=self.params['client_id'],
                code_verifier=sdata['code_verifier']
        )
        # !set header: 'Content-Type: application/x-www-form-urlencoded'
        tokenUrl = self.params['op_uris']['token_endpoint']
        tokenResponse = requests.post(tokenUrl, data=args)
        tdata =  tokenResponse.json()
        #print('*** token response', tdata)
        headers = dict(Authorization='Bearer ' + tdata['access_token'])
        userInfoUrl = self.params['op_uris']['userinfo_endpoint']
        userInfo = requests.get(userInfoUrl, headers=headers)
        userData = userInfo.json()
        #print('*** user data', userData)
        groupInfo = userData.get('urn:zitadel:iam:org:project:roles', {})
        #print('*** group info', groupInfo)
        groupInfo = userData.get('urn:zitadel:iam:org:project:roles')
        ndata = dict(
                userid=userData['preferred_username'],
                name=userData['name'],
                email=userData['email'],
                groups=list(groupInfo.keys()),
                access_token=tdata['access_token'],
        )
        self.storeSession(ndata)
        req.response.redirect(self.reqUrl, trusted=True)

    def logout(self):
        cname = self.params['cookie_name']
        logger.debug('logout, cookie: %s', cname)
        self.request.response.expireCookie(cname, path='/')
        self.request.response.redirect(config.base_url, trusted=True)

    def storeSession(self, data):
        lifetime = int(self.params['cookie_lifetime'])
        options = dict(
                path='/',
                expires=formatdate(time() + lifetime, localtime=False, usegmt=True),
                #httponly=True,
        )
        options['max-age'] = lifetime
        domain = self.params['cookie_domain']
        if domain:
            options['domain'] = domain
        name = self.params['cookie_name']
        value = json.dumps(data)
        #print('*** storeSession', name, value, options)
        if self.cookieCrypt:
            value = self.cookieCrypt.encrypt(value.encode('UTF-8')).decode('ASCII')
        self.request.response.setCookie(name, value, **options)

    def loadSession(self):
        cookie = self.request.getCookies().get(self.params['cookie_name'])
        if cookie is None:
            return {}
            #raise ValueError('Missing authentication cookie')
        if self.cookieCrypt:
            cookie = self.cookieCrypt.decrypt(cookie)
        #print('*** loadSession', self.params['cookie_name'], cookie)
        # !error check: return None - or raise error?
        data = json.loads(cookie)
        return data

    def loadOidcProviderData(self, force=False):
        if config.oidc_provider.startswith('test'):
            pass
        if force or self.params.get('op_uris') is None:
            uris = self.params['op_uris'] = {}
            opData = requests.get(self.params['op_config_url']).json()
            for key in self.oidcProviderUris:
                uris[key] = opData[key]
        if force or self.params.get('op_keys') is None:
            self.params['op_keys'] = requests.get(uris['jwks_uri']).json()['keys']


@register('auth', Root)
def authView(context, request):
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
    context.logout()
    return DefaultView(context, request)
