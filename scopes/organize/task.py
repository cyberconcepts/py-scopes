# scopes.organize.task

"""Task (and corresponding container) implementation."""

from scopes.storage.common import registerContainerClass
from scopes.storage.concept import Concept


class Task(Concept):

    headFields = ['name']
    prefix = 'tsk' 

