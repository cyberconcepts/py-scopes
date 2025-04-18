# scopes.storage.folder

from zope.interface import implementer

from scopes.interfaces import IContainer, IReference
from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track


class DummyFolder(dict):

    prefix = 'dummy'

    def asDict(self):
        return self

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, 
                             super(DummyFolder, self).__repr__())


@implementer(IContainer, IReference)
class Folder(Track):

    headFields = ['parent', 'name', 'ref']
    prefix = 'fldr'

    def values(self):
        return self.container.query(parent=self.rid)

    def items(self):
        return ((v.name, v) for v in self.values())

    def keys(self):
        return (v.name for v in self.values())

    def get(self, key, default=None):
        value = self.container.queryLast(parent=self.rid, name=key)
        if value is None:
            return default
        return value

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        value.set('parent', self.rid)
        value.set('name', key)
        self.container.save(value)

    def getTarget(self):
        if self.ref == '':
            return None
        return self.container.storage.getItem(self.ref)

    def setTarget(self, target):
        self.set('ref', target.uid)
        self.container.update(self)

    def __str__(self):
        return '%s: %s; keys: %s' % (self.__class__.__name__,
                self.name, list(self.keys()))


class Root(Folder):
    """A dummy (virtual) root folder for creating real folders
       using the Folder API."""

    prefix = 'root'

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
