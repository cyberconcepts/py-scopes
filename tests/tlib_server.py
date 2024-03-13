# tests/tlib_server.py

"""Test implementation for the `scopes.server` package."""

import json
from zope.publisher.browser import TestRequest
from zope.publisher.publish import publish

from scopes.server.app import Publication
from scopes.storage.folder import Root


def publishRequest(config, storage, path):
    appRoot = Root(storage)
    request = TestRequest(environ=dict(PATH_INFO=path))
    request.setPublication(Publication(appRoot))
    request = publish(request, False)
    return request.response


def test_app(self, config):
    storage = config.storageFactory(config.dbschema)
    response = publishRequest(config, storage, '/top')
    result = json.loads(response.consumeBody())
    self.assertEqual(result['items'][0]['head']['name'], 'child1')

