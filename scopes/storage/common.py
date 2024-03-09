# scopes.storage.common

"""Common utility stuff for the scopes.storage package."""

import base64
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy import Integer
from sqlalchemy.dialects.sqlite import JSON
import threading


# predefined db-specific definitions, usable for SQLite;
# may be overriden by import of ``scopes.storage.db.<dbname>``

def sessionFactory(engine):
    return engine.connect

def getEngine(dbtype, dbname, user, pw, host='localhost', port=5432, **kw):
    return create_engine('%s:///%s' % (dbtype, dbname), **kw)

def mark_changed(session):
    pass

def commit(conn):
    conn.commit()

IdType = Integer
JsonType = JSON


class StorageFactory(object):

    engine = Session = None

    sessionFactory = sessionFactory
    getEngine = getEngine
    mark_changed = mark_changed
    commit = commit
    IdType = IdType
    JsonType = JsonType

    def __call__(self, schema=None):
        st = Storage(schema=schema)
        st.setup(self)
        return st

    def setup(self, config):
        self.engine = self.getEngine(config.dbengine, config.dbname, 
                                     config.dbuser, config.dbpassword) 
        self.Session = self.sessionFactory


# you may put something like this in your code:
#scopes.storage.common.factory = StorageFactory(config)
# and then call at appropriate places:
#storage = scopes.storage.common.factory(schema=...)


class Storage(object):

    def __init__(self, schema=None):
        self.engine = engine
        self.session = Session()
        self.schema = schema
        self.metadata = MetaData(schema=schema)
        self.containers = {}

    def create(self, cls):
        container = cls(self)
        self.add(container)
        return container

    def add(self, container):
        self.containers[container.itemFactory.prefix] = container

    def getItem(self, uid):
        prefix, id = uid.split('-')
        id = int(id)
        container = self.containers.get(prefix)
        if container is None:
            container = self.create(registry[prefix])
        return container.get(id)

    def getExistingTable(self, tableName):
        metadata = self.metadata
        schema = self.schema
        metadata.reflect(self.engine)
        return metadata.tables.get((schema and schema + '.' or '') + tableName)

    def dropTable(self, tableName):
        with self.engine.begin() as conn:
            prefix = self.schema and self.schema + '.' or ''
            conn.execute(text('drop table if exists %s%s' % (prefix, tableName)))

    def resetSequence(self, tableName, colName, v):
        sq = ('alter sequence %s.%s_%s_seq restart %i' % 
                (self.schema, tableName, colName, v))
        with self.engine.begin() as conn:
            conn.execute(text(sq))


# store information about container implementations, identified by a uid prefix.

registry = {}

def registerContainerClass(cls):
    prefix = cls.itemFactory.prefix
    if prefix in registry:
        raise ValueError("prefix '%s' already registered!" % prefix)
    registry[prefix] = cls
    cls.headCols = cols = tuple(f.lower() for f in cls.itemFactory.headFields)
    if cls.indexes is None:
        cls.indexes = [cols[i:] for i in range(len(cols))]
    return cls

