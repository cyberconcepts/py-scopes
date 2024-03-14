# scopes.storage.concept

"""Core classes for concept map structure."""

from zope.interface import implementer
from scopes.interfaces import IConcept
from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track


@implementer(IConcept)
class Concept(Track):

    headFields = ['name']


class Concepts(Container):

    insertOnChange = False
 

class Predicate(Concept):

    prefix = 'pred'


@registerContainerClass
class Predicates(Concepts):

    itemFactory = Predicate
    tableName = 'preds'


class Triple(Track):

    headFields = ['first', 'second', 'predicate']
    prefix = 'rel'


@registerContainerClass
class Rels(Container):

    itemFactory = Triple
    indexes = [('first', 'predicate', 'second'),
               ('first', 'second'), ('predicate', 'second')]
    tableName = 'rels'
    insertOnChange = False


# types stuff

class Type(Concept):

    headFields = ['name', 'prefix']
    prefix = 'type'

    def get(key, default=None):
        return self.container.queryLast(name=key) or default


@registerContainerClass
class Types(Concepts):

    itemFactory = Type
    indexes = [('name',), ('prefix',)]
    tableName = 'types'
