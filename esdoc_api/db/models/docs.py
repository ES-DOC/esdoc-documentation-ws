# -*- coding: utf-8 -*-
"""
.. module:: docs.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: ES-DOC API db models - docs domain partition.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime
import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint

from esdoc_api.db.models.utils import Entity



# Domain model partition.
_DOMAIN_PARTITION = 'docs'

# Default drs split.
_DRS_SPLIT = '/'


class Document(Entity):
    """A document ingested into the ES-DOC API repository.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document'
    __table_args__ = (
        UniqueConstraint('project' ,'uid', 'version'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    # .. core fields
    project = Column(Unicode(63))
    sub_projects = Column(Unicode)
    institute = Column(Unicode(63))
    type = Column(Unicode(255), nullable=False)
    name = Column(Unicode(255), nullable=False)
    uid = Column(Unicode(63), nullable=False, default=uuid.uuid4())
    version = Column(Integer, nullable=False, default=1)
    ingest_date = Column(DateTime, default=datetime.datetime.now())
    is_latest = Column(Boolean, nullable=False, default=False)

    # .. summary fields
    canonical_name = Column(Unicode(1023))
    alternative_name = Column(Unicode(255))
    long_name = Column(Unicode(1023))
    description = Column(Unicode(1023))

    # .. inter-document fields
    model = Column(Unicode(1023))
    experiment = Column(Unicode(1023))


    def __init__(self):
        """Constructor.

        """
        super(Document, self).__init__()
        self.children = []
        self.as_obj = None


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.

        """
        return lambda instance: instance.canonical_name if instance.canonical_name else instance.uid + str(instance.version)


class DocumentDRS(Entity):
    """Encapsulates information required to resolve a document from DRS (directory reference syntax) info.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document_drs'
    __table_args__ = (
        UniqueConstraint('project' ,'document_id', 'path'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    document_id = Column(Integer,
                         ForeignKey('docs.tbl_document.id'), nullable=False)

    # Field set.
    project = Column(Unicode(63))
    path = Column(Unicode(511))
    key_01 = Column(Unicode(63))
    key_02 = Column(Unicode(63))
    key_03 = Column(Unicode(63))
    key_04 = Column(Unicode(63))
    key_05 = Column(Unicode(63))
    key_06 = Column(Unicode(63))
    key_07 = Column(Unicode(63))
    key_08 = Column(Unicode(63))


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.path


class DocumentExternalID(Entity):
    """The external id of a cim document.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document_external_id'
    __table_args__ = (
        UniqueConstraint('project' ,'document_id', 'external_id'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    document_id = Column(Integer,
                         ForeignKey('docs.tbl_document.id'), nullable=False)

    # Field set.
    project = Column(Unicode(63))
    external_id = Column(Unicode(255), nullable=False)


class DocumentSubProject(Entity):
    """Set of document sub-project references.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document_sub_project'
    __table_args__ = (
        UniqueConstraint('document_id', 'project', 'sub_project'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    document_id = Column(Integer,
                         ForeignKey('docs.tbl_document.id'), nullable=False)

    # Field set.
    project = Column(Unicode(63), nullable=False)
    sub_project = Column(Unicode(63), nullable=False)

