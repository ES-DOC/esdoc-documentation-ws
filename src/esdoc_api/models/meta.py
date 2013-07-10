"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


__all__ = ['Session', 'engine', 'metadata']


# SQlAlchemy database engine, updated by model.init_model()
engine = None

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())

# Global metadata. If you have multiple databases with
# overlapping table names, you'll need a metadata for
# each database
metadata = MetaData()

# IMPORTANT :: This imports all ES-DOC API types into the application scope.
from esdoc_api.lib.repo.models import *
from esdoc_api.lib.search import *
