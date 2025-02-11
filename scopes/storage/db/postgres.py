# scopes.storage.db.postgres

"""Database-related code specific for PostgreSQL."""

from sqlalchemy import create_engine
from sqlalchemy import BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import scoped_session, sessionmaker
import transaction
from zope.sqlalchemy import register, mark_changed

from scopes.storage.common import StorageFactory


class StorageFactory(StorageFactory):

    def sessionFactory(self):
        Session = scoped_session(sessionmaker(bind=self.engine, twophase=True))
        register(Session)
        return Session

    @staticmethod
    def getEngine(dbtype, dbname, user, pw, host='localhost', port=5432, **kw):
        return create_engine('%s://%s:%s@%s:%s/%s' % (
            dbtype, user, pw, host, port, dbname), **kw)

    def engineFromConfig(self, config):
        return self.getEngine(config.dbengine, config.dbname, 
                              config.dbuser, config.dbpassword,
                              host=getattr(config, 'dbhost', 'localhost'),
                              port=getattr(config, 'dbport', 5432))

    @staticmethod
    def mark_changed(session):
        return mark_changed(session)

    @staticmethod
    def commit(conn):
        transaction.commit()

    IdType = BigInteger
    JsonType = JSONB

