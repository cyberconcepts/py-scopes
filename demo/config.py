# py-scopes/demo/config.py

from dotenv import load_dotenv
import logging
from os import getenv
from scopes.web.app import zope_app_factory

load_dotenv()

log_file = 'log/scopes.log'
log_level = logging.DEBUG
log_format = '%(asctime)s %(levelname)s %(name)s %(message)s'
log_dateformat = '%Y-%m-%dT%H:%M:%S'
logging.basicConfig(filename=log_file, level=log_level, 
                    format=log_format, datefmt=log_dateformat)

server_port = getenv('SERVER_PORT', '8099')
base_url = getenv('BASE_URL', 'https://demo.cy7.de')

app_factory = zope_app_factory

# storage settings
from scopes.storage.db.postgres import StorageFactory
dbengine = 'postgresql+psycopg'
dbname = getenv('DBNAME', 'demo')
dbuser = getenv('DBUSER', 'demo')
dbpassword = getenv('DBPASSWORD', 'secret')
dbschema = getenv('DBSCHEMA', 'demo')

# authentication settings
oidc_provider = getenv('OIDC_PROVIDER', 'https://a1.cy7.de')
oidc_client_id = getenv('OIDC_CLIENT_ID', '311613119816392525')
oidc_params = dict(
    op_config_url=oidc_provider + '/.well-known/openid-configuration',
    op_uris=None,
    op_keys=None,
    callback_url=getenv('OIDC_CALLBACK_URL', base_url + '/auth/callback'),
    client_id = oidc_client_id,
    cookie_name=getenv('OIDC_COOKIE_NAME', 'oidc_' + oidc_client_id),
    cookie_domain=getenv('OIDC_COOKIE_DOMAIN', None),
    cookie_lifetime=getenv('OIDC_COOKIE_LIFETIME', '86400'),
    cookie_crypt=getenv('OIDC_COOKIE_CRYPT', None)
)

