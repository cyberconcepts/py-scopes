# py-scopes/tests/config.py

import logging
from os import getenv
import sys

#from scopes.web.app import demo_app, zope_app

log_file = 'scopes/tests/log/scopes-test.log'
log_level = logging.INFO
log_format = '%(asctime)s %(levelname)s %(name)s %(message)s'
log_dateformat = '%Y-%m-%dT%H:%M:%S'

def setup_logging():
    hdlr = logging.getLogger().handlers[-1]
    logging.getLogger().removeHandler(hdlr) # remove NullHandler added by testrunner
    logging.basicConfig(filename=log_file, level=log_level, 
                        format=log_format, datefmt=log_dateformat)

setup_logging()

# server / app settings
server_port = '8999'
base_url = 'testing:'
#app = zope_app

# storage settings

# SQLite
dbengine = 'sqlite'
dbname = 'var/test.db'
dbuser = None
dbpassword = None
dbschema = None

# special testing stuff
from scopes.tests import data_auth # add oidc URIs and keys to dummy_requests data
from scopes.tests import dummy_requests
sys.modules['requests'] = dummy_requests


# authentication settings
oidc_provider = 'test://oidc'
oidc_client_id = getenv('OIDC_CLIENT_ID', '12345')
oidc_params = dict(
    op_config_url=oidc_provider + '/.well-known/openid-configuration',
    op_uris=None,
    op_keys=None,
    op_project_scope='urn:zitadel:iam:org:project:id:zitadel:aud',
    callback_url=getenv('OIDC_CALLBACK_URL', base_url + '/auth/callback'),
    client_id=oidc_client_id,
    principal_prefix=getenv('OIDC_PRINCIPAL_PREFIX', 'loops.'),
    cookie_name=getenv('OIDC_COOKIE_NAME', 'oidc_' + oidc_client_id),
    cookie_domain=getenv('OIDC_COOKIE_DOMAIN', None),
    cookie_lifetime=getenv('OIDC_COOKIE_LIFETIME', '86400'),
    cookie_crypt=getenv('OIDC_COOKIE_CRYPT', None),
    private_key_file=getenv('OIDC_SERVICE_USER_PRIVATE_KEY_FILE', 
                            'scopes/tests/test-private-key.json'),
    organization_id=getenv('OIDC_ORGANIZATION_ID', '12346'),
    project_id=getenv('OIDC_PROJECT_ID', '12347'),
)

oidc_provider_endpoints = dict(
    user='v2/users/human',
)
