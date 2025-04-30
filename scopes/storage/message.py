# scopes.storage.message

"""Generic messages (or events) to be stored in SQL database."""

from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track

class Message(Track):

    headFields = ['domain', 'action', 'class', 'item']
    prefix = 'msg'


@registerContainerClass
class Messages(Container):

    itemFactory = Message
    indexes = [('domain', 'action', 'class', 'item'), ('domain', 'class', 'item')]
    tableName = 'messages'
    insertOnChange = True
