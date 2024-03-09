# scopes.storage.folder

from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track


class Folder(Track):

    headFields = ['parent', 'name', 'ref']
    prefix = 'fldr'

    def keys(self):
        for f in self.container.query(parent=self.rid):
            yield f.name

    def get(self, key, default=None):
        value = self.container.queryLast(parent=self.rid, name=key)
        if value is None:
            return default
        return value

    def __getitem__(self, key):
        value = self.container.queryLast(parent=self.rid, name=key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        value.set('parent', self.rid)
        value.set('name', key)
        self.container.save(value)


class Root(Folder):
    """A dummy (virtual) root folder for creating real folders
       using the Folder API."""

    def __init__(self, storage):
        cont = storage.create(Folders)
        super(Root, self).__init__(container=cont)

    uid = ''


@registerContainerClass
class Folders(Container):

    itemFactory = Folder
    indexes = [('parent', 'name'), ('ref',)]
    tableName = 'folders'
    insertOnChange = False
