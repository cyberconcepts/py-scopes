# scopes.storage.folder

from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track


class Folder(Track):

    headFields = ['parent', 'name', 'ref']
    prefix = 'fldr'

    def keys(self):
        for f in self.container.query(parent=self.uid):
            yield f.name

    def get(self, key, default=None):
        value = self.container.queryLast(parent=self.uid, name=key)
        if value is None:
            return default
        return value

    def __getitem__(self, key):
        value = self.container.queryLast(parent=self.uid, name=key)
        if value is None:
            raise KeyError
        return value

    def __setitem__(self, key, value):
        value.head['parent'] = self.uid
        value.head['name']= key
        self.container.save(value)


@registerContainerClass
class Folders(Container):

    itemFactory = Folder
    indexes = [('parent', 'name'), ('ref',)]
    tableName = 'folders'
    insertOnChange = False
