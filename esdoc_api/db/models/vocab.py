# -*- coding: utf-8 -*-
"""
.. module:: vocab.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: ES-DOC API db models - vocab domain partition.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Unicode,
    UniqueConstraint,
)

from esdoc_api.db.models.utils import Entity



# Constants pertaining to document types.
DOCUMENT_TYPE_ALL = '*'

# Domain model partition.
_DOMAIN_PARTITION = 'vocab'


class DocumentEncoding(Entity):
    """An encoding with which a document representation maybe associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document_encoding'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    encoding = Column(Unicode(63), nullable=False, unique=True)


    @property
    def cache_name(self):
        """Gets instance cache key name.

        """
        return self.encoding


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.encoding


class DocumentType(Entity):
    """Meta-information regarding the type of document.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_document_type'
    __table_args__ = (
        UniqueConstraint('key'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    ontology = Column(Unicode(63), nullable=False)
    key = Column(Unicode(255), nullable=False)
    display_name = Column(Unicode(63), nullable=False)
    is_search_target = Column(Boolean, nullable=False, default=True)
    is_pdf_target = Column(Boolean, nullable=False, default=True)


    @property
    def cache_name(self):
        """Gets instance cache key name.

        """
        return self.key


class Institute(Entity):
    """Represents an institute with which documents are associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_institute'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    name = Column(Unicode(16), nullable=False, unique=True)
    long_name = Column(Unicode(512), nullable=False)
    country_code = Column(Unicode(2), nullable=False)
    url = Column(Unicode(256))


    @property
    def cache_name(self):
        """Gets instance cache key name.

        """
        return self.name


    @property
    def FullName(self):
        """Gets the full institute name derived by concatanation.

        """
        return self.country_code + u" - " + self.name + u" - " + self.long_name


class Project(Entity):
    """Represents a project with which documents are associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tbl_project'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    name = Column(Unicode(63), nullable=False, unique=True)
    description = Column(Unicode(1023))
    url = Column(Unicode(1023))


    @property
    def cache_name(self):
        """Gets instance cache key name.

        """
        return self.name
