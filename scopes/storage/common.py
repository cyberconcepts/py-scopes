# scopes.storage.common

"""Common utility stuff for the scopes.storage package."""

import base64
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy import Integer
from sqlalchemy.dialects.sqlite import JSON
import threading


class Storage(object):

    def __init__(self, db, schema=None):
        self.db = db
        self.engine = db.engine
        self.session = db.Session()
        self.schema = schema
        self.metadata = MetaData(schema=schema)
        self.containers = {}

    def commit(self):
        self.db.commit(self.session)

    def mark_changed(self):
        self.db.mark_changed(self.session)

    def create(self, cls):
        container = cls(self)
        self.add(container)
        return container

    def add(self, container):
        self.containers[container.itemFactory.prefix] = container

    def getContainer(self, itemClass):
        prefix = itemClass.prefix
        container = self.containers.get(prefix)
        if container is None:
            return self.create(registry[prefix])
        return container

    def getItem(self, uid):
        prefix, id = uid.split('-')
        cls = registry[prefix].itemFactory
        return self.getContainer(cls).get(int(id))

    def getExistingTable(self, tableName):
        metadata = self.metadata
        schema = self.schema
        metadata.reflect(self.engine)
        return metadata.tables.get((schema and schema + '.' or '') + tableName)

    def dropTable(self, tableName):
        prefix = self.schema and self.schema + '.' or ''
        with self.engine.begin() as conn:
            conn.execute(text('drop table if exists %s%s' % (prefix, tableName)))

    def resetSequence(self, tableName, colName, v):
        sq = ('alter sequence %s.%s_%s_seq restart %i' % 
                (self.schema, tableName, colName, v))
        with self.engine.begin() as conn:
            conn.execute(text(sq))


class StorageFactory:

    def sessionFactory(self):
         return self.engine.connect

    @staticmethod
    def getEngine(dbtype, dbname, user, pw, **kw):
        return create_engine('%s:///%s' % (dbtype, dbname), **kw)

    def engineFromConfig(self, config):
        return self.getEngine(config.dbengine, config.dbname, 
                              config.dbuser, config.dbpassword) 

    @staticmethod
    def mark_changed(session):
        pass

    @staticmethod
    def commit(conn):
        conn.commit()

    IdType = Integer
    JsonType = JSON

    storageClass = Storage

    def __init__(self, config, storageClass=None):
        self.engine = self.engineFromConfig(config)
        self.Session = self.sessionFactory()
        if storageClass is not None:
            self.storageClass = storageClass

    def __call__(self, schema=None):
        return self.storageClass(self, schema=schema)


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

