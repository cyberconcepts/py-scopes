# scopes.web.client

"""Web client functionality: access to web sites, APIs with authentication."""

import requests

import config


class ApiClient:

    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        self.authToken = None

    def authentication(self):
        if self.authToken == None:
            self.authToken = oidc.authenticateClient()
        return dict(Authorization=f'Bearer {self.authToken}')

    def post(self, endpoint, data):
        headers = self.authentication()
        # self.makeUrl(endpoint)
        url = '/'.join(self.baseUrl, endpoint)
        resp = requests.post(url, data=data, headers=headers)
        # check: resp.status_code
        data = resp.json()
        return data

