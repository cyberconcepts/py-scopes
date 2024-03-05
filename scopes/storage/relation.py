# scopes.storage.relation

"""An SQL-based relationship engine using RDF-like triples."""

from scopes.storage.common import registerContainerClass
from scopes.storage.tracking import Container, Track


class Triple(Track):

    headFields = ['first', 'second', 'pred']
    prefix = 'rel'
 
