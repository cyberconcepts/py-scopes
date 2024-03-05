# scopes.storage.concept

"""Abstract base classes for concept map application classes."""

from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track


class Concept(Track):

    headFields = ['parent', 'name']
 
