# py-scopes/tests/config.py

from scopes.server.app import demo_app, zope_app

# server / app settings
server_port = '8999'
app = zope_app

# storage settings
dbengine = 'postgresql+psycopg'
dbname = 'testdb'
dbuser = 'testuser'
dbpassword = 'secret'

