"""
.. module:: esdoc_api.models.vocab.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The controlled vocabulary set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    UniqueConstraint,
)

from esdoc_api.models.utils import (
    create_fk,
    Entity
    )



# Module exports.
__all__ = [
    'DocumentEncoding',
    'DocumentLanguage',
    'DocumentOntology',
    'DocumentType',
    'DOCUMENT_TYPE_ALL',
    'INGEST_STATES',
    'INGEST_STATE_QUEUED',
    'INGEST_STATE_RUNNING',
    'INGEST_STATE_SUSPENDED',
    'INGEST_STATE_COMPLETE',
    'INGEST_STATE_ERROR',
    'INGEST_STATE_QUEUED_ID',
    'INGEST_STATE_RUNNING_ID',
    'INGEST_STATE_SUSPENDED_ID',
    'INGEST_STATE_COMPLETE_ID',
    'INGEST_STATE_ERROR_ID',
    'IngestState',
    'Institute',
    'Project'
]



# Constants pertaining to document types.
DOCUMENT_TYPE_ALL = '*'


# Constants pertaining to states.
INGEST_STATE_COMPLETE = "COMPLETE"
INGEST_STATE_COMPLETE_ID = 4
INGEST_STATE_ERROR = "ERROR"
INGEST_STATE_ERROR_ID = 5
INGEST_STATE_QUEUED = "QUEUED"
INGEST_STATE_QUEUED_ID = 1
INGEST_STATE_RUNNING = "RUNNING"
INGEST_STATE_RUNNING_ID = 2
INGEST_STATE_SUSPENDED = "SUSPENDED"
INGEST_STATE_SUSPENDED_ID = 3
INGEST_STATES = (
    INGEST_STATE_COMPLETE,
    INGEST_STATE_ERROR,
    INGEST_STATE_QUEUED,
    INGEST_STATE_RUNNING,
    INGEST_STATE_SUSPENDED,
)
INGEST_STATE_IDS = (
    INGEST_STATE_COMPLETE_ID,
    INGEST_STATE_ERROR_ID,
    INGEST_STATE_QUEUED_ID,
    INGEST_STATE_RUNNING_ID,
    INGEST_STATE_SUSPENDED_ID,
)


# Domain model partition.
_DOMAIN_PARTITION = 'vocab'


class DocumentEncoding(Entity):
    """An encoding with which a document representation maybe associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentEncoding'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    Encoding = Column(Unicode(63), nullable=False, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Encoding


class DocumentLanguage(Entity):
    """A language with which a document is associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentLanguage'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    Code = Column(Unicode(2), nullable=False)
    Name =  Column(Unicode(127), nullable=False, unique=True)


    @property
    def FullName(self):
        """Gets the full language name derived by concatanation.
        
        """
        return self.Code + u" - " + self.Name


class DocumentOntology(Entity):
    """An ontology with which a document is associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentOntology'
    __table_args__ = (
        UniqueConstraint('Name' ,'Version'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    Name = Column(Unicode(63), nullable=False)
    Version = Column(Unicode(31), nullable=False)


    @property
    def FullName(self):
        """Gets the full ontology name.

        """
        result = self.Name
        result += '-v'
        result += self.Version
        return result


class DocumentType(Entity):
    """Meta-information regarding the type of document.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentType'
    __table_args__ = (
        UniqueConstraint('Key'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Ontology_ID = create_fk('vocab.tblDocumentOntology.ID', required=True)

    # Field set.
    Key = Column(Unicode(255), nullable=False)
    DisplayName = Column(Unicode(63), nullable=False)


class IngestState(Entity):
    """The state that a ingest process may be in, i.e. InProgress, Queued, Error...etc.
    
    """
    # SQLAlchemy directives.
    __tablename__ = 'tblIngestState'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    Name =  Column(Unicode(16), nullable=False, unique=True)
    Description =  Column(Unicode(128), nullable=False)
    Code =  Column(Integer, nullable=False, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.
        
        """
        return lambda instance: instance.Code


class Institute(Entity):
    """Represents an institute with which documents are associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblInstitute'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    Name =  Column(Unicode(16), nullable=False, unique=True)
    LongName =  Column(Unicode(512), nullable=False)
    CountryCode = Column(Unicode(2), nullable=False)
    URL =  Column(Unicode(256))


    @property
    def FullName(self):
        """Gets the full institute name derived by concatanation.

        """
        return self.CountryCode + u" - " + self.Name + u" - " + self.LongName


class Project(Entity):
    """Represents a project with which documents are associated.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblProject'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    Name =  Column(Unicode(16), nullable=False, unique=True)
    Description =  Column(Unicode(1023))
    URL =  Column(Unicode(1023))
