# py-scopes/tests/config.py

from scopes.server.app import demo_app, zope_app

# server / app settings
server_port = '8999'
app = zope_app

# storage settings

# PostgreSQL
import scopes.storage.db.postgres
dbengine = 'postgresql+psycopg'
dbname = 'testdb'
dbuser = 'testuser'
dbpassword = 'secret'
dbschema = 'testing'

# SQLite
#dbengine = 'sqlite'
#dbname = 'var/test.db'
#dbschema = None

