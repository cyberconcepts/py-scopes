# scopes.tests.requests

"""Dummy requests implementation for testing."""

from logging import getLogger
logger = getLogger('tests.dummy_requests')

def get(url, *args, **kw):
    logger.info(f'get: %s - %s - %s', url, args, kw)
    return FakeResponse(response_data[url])


class FakeResponse:

    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


response_data = {}
