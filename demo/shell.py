# scopes/demo/shell.py
# simple shell for interactive testing / accessing the database (storage)
# use: `python -i shell.py`

import config
from scopes.web.auth import oidc
from scopes.storage.folder import Root
from scopes.storage import topic

storage = config.StorageFactory(config)(config.dbschema)
root = Root(storage)
