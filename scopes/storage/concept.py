# scopes.storage.concept

"""Core classes for concept map structure."""

from zope.interface import implementer
from scopes.interfaces import IContainer
from scopes.storage.common import registerContainerClass, registry
from scopes.storage.tracking import Container, Track


class Concept(Track):

    headFields = ['name']

    def parents(self, predicate=None):
        return self.container.queryRels(second=self, predicate=predicate)

    def children(self, predicate=None):
        return self.container.queryRels(first=self, predicate=predicate)

    def values(self):
       return (t.getSecond() for t in  self.children(Rels.defaultPredicate))


class Concepts(Container):

    insertOnChange = False
    indexes = None

    def queryRels(self, **crit):
        pred = crit.get(predicate)
        if pred is not None and isinstance(pred, ('string', 'bytes')):
            crit['predicate'] = self.storage.getContainer(Predicate).queryLast(name=pred)
        for k, v in crit.items:
            if isinstance(v, Track):
                crit[k] = v.uid
        rels = self.storage.getContainer(Triple)
        return rels.query(**crit)
 

 # implementation of relationships between concepts using RDF-like triples

class Predicate(Concept):

    prefix = 'pred'


@registerContainerClass
class Predicates(Concepts):

    itemFactory = Predicate
    tableName = 'preds'


defaultPredicate = 'standard'

def storePredicate(storage, name):
    preds = storage.getContainer(Predicate)
    preds.save(Predicate(name))


class Triple(Track):

    headFields = ['first', 'second', 'predicate']
    prefix = 'rel'

    def getFirst(self):
        return self.container.storage.getItem(self.first)

    def getSecond(self):
        return self.container.storage.getItem(self.second)

    def getPredicate(self):
        return self.container.storage.getItem(self.second)


@registerContainerClass
class Rels(Container):

    itemFactory = Triple
    indexes = [('first', 'predicate', 'second'),
               ('first', 'second'), ('predicate', 'second')]
    tableName = 'rels'
    insertOnChange = False


# types stuff

@implementer(IContainer)
class Type(Concept):

    headFields = ['name', 'tprefix']
    prefix = 'type'

    @property
    def typeClass(self):
        return registry[self.tprefix].itemFactory

    def values(self):
        cont = self.container.storage.getContainer(self.typeClass)
        return cont.query()

    def get(self, key, default=None):
        cont = self.container.storage.getContainer(self.typeClass)
        return cont.queryLast(name=key) or default

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        cont = self.container.storage.getContainer(self.typeClass)
        value.name = key
        cont.save(value)


@registerContainerClass
class Types(Concepts):

    itemFactory = Type
    indexes = [('name',), ('tprefix',)]
    tableName = 'types'


def storeType(storage, cls, name):
    types = storage.getContainer(Type)
    types.save(Type(name, cls.prefix))

def setupCoreTypes(storage):
    for c in registry.values():
        cls = c.itemFactory
        storeType(storage, cls, cls.__name__.lower())

