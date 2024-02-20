# py-scopes/demo/main.py

import config

from app import demo_app
import server

server.run(demo_app, config)

