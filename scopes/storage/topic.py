# scopes.storage.topic

from scopes.storage.common import registerContainerClass
from scopes.storage import concept

class Topic(concept.Concept):

    prefix = 'tpc'


@registerContainerClass
class Topics(concept.Concepts):

    itemFactory = Topic
    tableName = 'topics'



