# scopes.storage.db.postgres

"""Database-related code specific for PostgreSQL."""

from sqlalchemy import create_engine
from sqlalchemy import BigInteger, JSONB
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import scoped_session, sessionmaker
import transaction
from zope.sqlalchemy import register, mark_changed


def sessionFactory(engine):
    Session = scoped_session(sessionmaker(bind=engine, twophase=True))
    register(Session)
    return Session

def getEngine(dbtype, dbname, user, pw, host='localhost', port=5432, **kw):
    return create_engine('%s://%s:%s@%s:%s/%s' % (
        dbtype, user, pw, host, port, dbname), **kw)

def commit(conn):
    transaction.commit()
