# scopes.storage.db.postgres

"""Database-related code specific for PostgreSQL."""

from sqlalchemy import create_engine
from sqlalchemy import BigInteger
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

import scopes.storage.common
scopes.storage.common.IdType = BigInteger
scopes.storage.common.JsonType = JSONB
scopes.storage.common.sessionFactory = sessionFactory
scopes.storage.common.getEngine = getEngine
scopes.storage.common.mark_changed = mark_changed
scopes.storage.common.commit = commit

