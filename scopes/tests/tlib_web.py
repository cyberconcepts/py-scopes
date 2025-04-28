# tests/tlib_web.py

"""Test implementation for the `scopes.web` package."""

import json
import logging
from zope.publisher.browser import TestRequest
from zope.publisher.publish import publish

from scopes.web.app import Publication
from scopes.storage.folder import Root

logger = logging.getLogger('tlib_web')


def publishRequest(config, storage, path):
    appRoot = Root(storage)
    request = TestRequest(environ=dict(PATH_INFO=path))
    request.setPublication(Publication(appRoot))
    request = publish(request, False)
    return request.response


def test_app(self, config):
    storage = config.storageFactory(config.dbschema)
    response = publishRequest(config, storage, '/top')
    logger.info('test_app: response %s %s', response.getStatus(), response.getHeaders())
    result = json.loads(response.consumeBody())
    self.assertEqual(result['items'][0]['head']['name'], 'level2-item1')

def test_auth(self, config):
    from scopes.web.auth import oidc
    oidc.startup()  # todo: use generic app.startServices()
    self.assertEqual(len(config.oidc_params['op_uris']), 8)
    storage = config.storageFactory(config.dbschema)
    response = publishRequest(config, storage, '/top/auth/login')
    headers = dict(response.getHeaders())
    logger.info('test_auth: response %s %s', response.getStatus(), headers)
    self.assertEqual(response.getStatus(), 302)
