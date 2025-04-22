# tests/tlib_web.py

"""Test implementation for the `scopes.web` package."""

import json
import logging
from zope.publisher.browser import TestRequest
from zope.publisher.publish import publish

from scopes.web.app import Publication
from scopes.storage.folder import Root


def publishRequest(config, storage, path):
    appRoot = Root(storage)
    request = TestRequest(environ=dict(PATH_INFO=path))
    request.setPublication(Publication(appRoot))
    request = publish(request, False)
    return request.response


def test_app(self, config):
    logger = logging.getLogger('tlib_web')
    logger.info('test_app')
    storage = config.storageFactory(config.dbschema)
    response = publishRequest(config, storage, '/top')
    print('***', response.getStatus(), response.getHeaders())
    result = json.loads(response.consumeBody())
    self.assertEqual(result['items'][0]['head']['name'], 'level2-item1')

