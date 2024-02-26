# scopes.storage.folder

from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track


class Folder(Track):

    headFields = ['parent', 'name']
    prefix = 'fldr'

    def keys(self):
        return []

    def get(self, key, default=None):
        return default

    def __getitem__(self, key):
        raise KeyError


@registerContainerClass
class Folders(Container):

    itemFactory = Folder
    indexes = [('parent', 'name')]
    tableName = 'folders'
    insertOnChange = False
