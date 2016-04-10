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

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    DateTime,
    Integer,
    Unicode,
    UniqueConstraint
    )
from sqlalchemy.orm import relationship

from esdoc_api.db.models.utils import (
    Entity,
    EntityConvertor
    )



# Module exports.
__all__ = [
    'Document',
    'DocumentDRS',
    'DocumentExternalID',
    'DocumentSummary',
    'DOCUMENT_VERSIONS',
    'DOCUMENT_VERSION_LATEST',
    'DOCUMENT_VERSION_ALL'
]



# Domain model partition.
_DOMAIN_PARTITION = 'docs'

# Default drs split.
_DRS_SPLIT = '/'

# Document version related constants.
DOCUMENT_VERSION_ALL = '*'
DOCUMENT_VERSION_LATEST = 'latest'
DOCUMENT_VERSIONS = [DOCUMENT_VERSION_ALL, DOCUMENT_VERSION_LATEST]


class Document(Entity):
    """A document ingested into the ES-DOC API repository.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document'
    __table_args__ = (
        UniqueConstraint('project_id' ,'uid', 'version'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    project_id = Column(Integer,
                        ForeignKey('vocab.tbl_project.ID'), nullable=False)
    institute_id = Column(Integer,
                          ForeignKey('vocab.tbl_institute.ID'))

    # Relationships.
    ExternalIDs = relationship("DocumentExternalID", backref="Document")
    Summaries = relationship("DocumentSummary", backref="Document", lazy='joined')

    # Field set.
    source = Column(Unicode(255))
    type = Column(Unicode(255), nullable=False)
    name = Column(Unicode(255), nullable=False)
    uid = Column(Unicode(63), nullable=False, default=uuid.uuid4())
    version = Column(Integer, nullable=False, default=1)
    ingest_date = Column(DateTime, default=datetime.datetime.now())
    is_latest = Column(Boolean, nullable=False, default=False)
    sub_project = Column(Unicode(255))


    def __init__(self):
        """Constructor.

        """
        super(Document, self).__init__()
        self.children = []
        self.as_obj = None


    @property
    def summary(self):
        """Gets top summary from associated collection.

        """
        if self.Summaries is not None or len(self.Summaries) > 0:
            return self.Summaries[0]
        else:
            return None


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.

        """
        return lambda instance: instance.uid + str(instance.version)


class DocumentDRS(Entity):
    """Encapsulates information required to resolve a document from DRS (directory reference syntax) info.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document_drs'
    __table_args__ = (
        UniqueConstraint('project_id' ,'document_id', 'path'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    project_id = Column(Integer,
                        ForeignKey('vocab.tbl_project.ID'), nullable=False)
    document_id = Column(Integer,
                         ForeignKey('docs.tbl_document.ID'), nullable=False)

    # Field set.
    path = Column(Unicode(511))
    key_01 = Column(Unicode(63))
    key_02 = Column(Unicode(63))
    key_03 = Column(Unicode(63))
    key_04 = Column(Unicode(63))
    key_05 = Column(Unicode(63))
    key_06 = Column(Unicode(63))
    key_07 = Column(Unicode(63))
    key_08 = Column(Unicode(63))


    def clone(self):
        """Returns a cloned instance.

        """
        result = DocumentDRS()

        result.document_id = self.document_id
        result.key_01 = self.key_01
        result.key_02 = self.key_02
        result.key_03 = self.key_03
        result.key_04 = self.key_04
        result.key_05 = self.key_05
        result.key_06 = self.key_06
        result.key_07 = self.key_07
        result.key_08 = self.key_08
        result.path = self.path
        result.project_id = self.project_id

        return result


    def reset_path(self):
        """Resets drs path based upon value of keys.

        """
        path = ''
        for i in range(8):
            key = getattr(self, "key_0" + str(i + 1))
            if key is not None:
                if i > 0:
                    path += _DRS_SPLIT
                path += key.upper()
        self.path = path


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
        UniqueConstraint('project_id' ,'document_id', 'external_id'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    project_id = Column(Integer,
                        ForeignKey('vocab.tbl_project.ID'), nullable=False)
    document_id = Column(Integer,
                         ForeignKey('docs.tbl_document.ID'), nullable=False)

    # Field set.
    external_id = Column(Unicode(255), nullable=False)


class DocumentSummary(Entity):
    """Encapsulates document summary information.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document_summary'
    __table_args__ = (
        UniqueConstraint('document_id' ,'language_id'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    document_id = Column(Integer,
                         ForeignKey('docs.tbl_document.ID'), nullable=False)
    language_id = Column(Integer,
                         ForeignKey('vocab.tbl_document_language.ID'), nullable=False)

    # Field set.
    short_name = Column(Unicode(1023))
    long_name = Column(Unicode(1023))
    description = Column(Unicode(1023))
    field_01 = Column(Unicode(1023))
    field_02 = Column(Unicode(1023))
    field_03 = Column(Unicode(1023))
    field_04 = Column(Unicode(1023))
    field_05 = Column(Unicode(1023))
    field_06 = Column(Unicode(1023))
    field_07 = Column(Unicode(1023))
    field_08 = Column(Unicode(1023))
    model = Column(Unicode(1023))
    experiment = Column(Unicode(1023))


    def format_dict(self, as_dict, key_formatter=None, json_formatting=False):
        """Formats a dictionary representation.

        """
        as_dict['document'] = \
            EntityConvertor.to_dict(self.Document, key_formatter, json_formatting)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.short_name

