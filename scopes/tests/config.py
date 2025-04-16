# py-scopes/tests/config.py

import logging
from os import getenv

#from scopes.server.app import demo_app, zope_app

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

# authentication settings
oidc_provider = 'testing:'
oidc_client_id = getenv('OIDC_CLIENT_ID', '12345')
oidc_params = dict(
    auth_url=getenv('OIDC_PROVIDER_URL', oidc_provider + '/oauth/v2/authorize'),
    token_url=getenv('OIDC_TOKEN_URL', oidc_provider + '/oauth/v2/token'),
    userinfo_url=getenv('OIDC_USERINFO_URL', oidc_provider + '/oidc/v1/userinfo'),
    callback_url=getenv('OIDC_CALLBACK_URL', base_url + '/auth_callback'),
    client_id=oidc_client_id,
    principal_prefix=getenv('OIDC_PRINCIPAL_PREFIX', 'loops.'),
    cookie_name=getenv('OIDC_COOKIE_NAME', 'oidc_' + oidc_client_id),
    cookie_domain=getenv('OIDC_COOKIE_DOMAIN', None),
    cookie_lifetime=getenv('OIDC_COOKIE_LIFETIME', '86400'),
    cookie_crypt=getenv('OIDC_COOKIE_CRYPT', None)
)

