# py-scopes/demo/config.py

from dotenv import load_dotenv
from os import getenv
from scopes.server.app import demo_app, zope_app

load_dotenv()

server_port = getenv('SERVER_PORT', '8099')

app = zope_app

# storage settings
dbengine = 'postgresql+psycopg'
dbname = getenv('DBNAME', 'demo')
dbuser = getenv('DBUSER', 'demo')
dbpassword = getenv('DBPASSWORD', 'secret')

