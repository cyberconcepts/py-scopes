# py-scopes/demo/config.py

from dotenv import load_dotenv
from os import getenv
from scopes.server.app import zope_app_factory

load_dotenv()

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
oidc_provider = 'https://a1.cy7.de'
oidc_client_id = getenv('OIDC_CLIENT_ID', '311613119816392525')
oidc_params = dict(
    auth_url=getenv('OIDC_PROVIDER_URL', oidc_provider + '/oauth/v2/authorize'),
    callback_url=getenv('OIDC_CALLBACK_URL', base_url + '/auth/callback'),
    client_id = oidc_client_id,
    cookie_name=getenv('OIDC_COOKIE_NAME', 'oidc_' + oidc_client_id),
    cookie_domain=getenv('OIDC_COOKIE_DOMAIN', 'cy7.de'),
    cookie_lifetime=getenv('OIDC_COOKIE_LIFETIME', '86400'),
)

