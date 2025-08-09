# scopes.web.client

"""Web client functionality: access to web sites, APIs with authentication."""

import logging
import requests
from scopes.web.auth import oidc

logger = logging.getLogger('web.client')


class ApiClient:

    def __init__(self, baseUrl, authToken=None):
        self.baseUrl = baseUrl
        self.authToken = authToken

    def authentication(self):
        if self.authToken == None:
            self.authToken = oidc.authenticateClient()
        return dict(Authorization=f'Bearer {self.authToken}')

    def post(self, endpoint, data):
        headers = self.authentication()
        headers['Content-Type'] = 'application/json'
        headers['Connect-Protocol-Version'] = '1'
        # self.makeUrl(endpoint)
        url = '/'.join((self.baseUrl, endpoint))
        resp = requests.post(url, json=data, headers=headers)
        if resp.status_code >= 400:
            logger.error('post %s: %s %s', url, resp.status_code, resp.text)
        return resp.status_code, resp.json()

    def put(self, endpoint, objId, data):
        headers = self.authentication()
        headers['Content-Type'] = 'application/json'
        # self.makeUrl(endpoint, objId)
        url = '/'.join((self.baseUrl, endpoint, objId))
        resp = requests.put(url, json=data, headers=headers)
        if resp.status_code >= 400:
            logger.error('post %s: %s %s', url, resp.status_code, resp.text)
        return resp.status_code, resp.json()

