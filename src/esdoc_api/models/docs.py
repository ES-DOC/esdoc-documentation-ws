"""
.. module:: esdoc_api.models.docs.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The controlled vocabulary set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import datetime
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Text,
    Unicode,
    UniqueConstraint
    )
from sqlalchemy.orm import relationship

from esdoc_api.models.utils import (
    create_fk,
    Entity
    )


# Module exports.
__all__ = [
    'Document',
    'DocumentDRS',
    'DocumentExternalID',
    'DocumentRepresentation',
    'DocumentSubDocument',
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
DOCUMENT_VERSION_LATEST = 'LATEST'
DOCUMENT_VERSIONS = [DOCUMENT_VERSION_ALL, DOCUMENT_VERSION_LATEST]


class Document(Entity):
    """A document ingested into the ES-DOC API repository.
    
    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocument'
    __table_args__ = (
        UniqueConstraint('Project_ID' ,'UID', 'Version'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Project_ID = create_fk('vocab.tblProject.ID', required=True)
    Institute_ID = create_fk('vocab.tblInstitute.ID')
    IngestEndpoint_ID = create_fk('ingest.tblIngestEndpoint.ID')
    #Type_ID = create_fk('vocab.tblDocumentType.ID', required=True)
    
    # Relationships.
    ExternalIDs = relationship("DocumentExternalID", backref="Document")
    Summaries = relationship("DocumentSummary", backref="Document", lazy='joined')
    Representations = relationship("DocumentRepresentation", backref="Document")

    # Field set.
    Type =  Column(Unicode(63), nullable=False)
    Name =  Column(Unicode(255), nullable=False)
    UID = Column(Unicode(63), nullable=False, default=uuid.uuid4())
    Version = Column(Integer, nullable=False, default=1)
    HasChildren = Column(Boolean, nullable=False, default=False)
    IsChild = Column(Boolean, nullable=False, default=False)
    IsLatest = Column(Boolean, nullable=False, default=False)
    IsIndexed = Column(Boolean, nullable=False, default=False)
    IngestDate =  Column(DateTime, default=datetime.datetime.now())


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
        return lambda instance: instance.UID + str(instance.Version)


class DocumentDRS(Entity):
    """Encapsulates information required to resolve a document from DRS (directory reference syntax) info.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentDRS'
    __table_args__ = (
        UniqueConstraint('Project_ID' ,'Document_ID', 'Path'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Project_ID = create_fk('vocab.tblProject.ID', required=True)
    Document_ID = create_fk('docs.tblDocument.ID', required=True)

    # Field set.
    Path = Column(Unicode(511))
    Key_01 = Column(Unicode(63))
    Key_02 = Column(Unicode(63))
    Key_03 = Column(Unicode(63))
    Key_04 = Column(Unicode(63))
    Key_05 = Column(Unicode(63))
    Key_06 = Column(Unicode(63))
    Key_07 = Column(Unicode(63))
    Key_08 = Column(Unicode(63))


    def clone(self):
        """Returns a cloned instance.

        """
        result = DocumentDRS()

        result.Document_ID = self.Document_ID
        result.Key_01 = self.Key_01
        result.Key_02 = self.Key_02
        result.Key_03 = self.Key_03
        result.Key_04 = self.Key_04
        result.Key_05 = self.Key_05
        result.Key_06 = self.Key_06
        result.Key_07 = self.Key_07
        result.Key_08 = self.Key_08
        result.Path = self.Path
        result.Project_ID = self.Project_ID

        return result


    def reset_path(self):
        """Resets drs path based upon value of keys.

        """
        path = ''
        for i in range(8):
            key = getattr(self, "Key_0" + str(i + 1))
            if key is not None:
                if i > 0:
                    path += _DRS_SPLIT
                path += key.upper()
        self.Path = path


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Path


class DocumentExternalID(Entity):
    """The external id of a cim document.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentExternalID'
    __table_args__ = (
        UniqueConstraint('Project_ID' ,'Document_ID', 'ExternalID'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Project_ID = create_fk('vocab.tblProject.ID', required=True)
    Document_ID = create_fk('docs.tblDocument.ID', required=True)

    # Field set.
    ExternalID = Column(Unicode(255), nullable=False)


class DocumentRepresentation(Entity):
    """A document representation in one of the supported encodings.
    
    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentRepresentation'
    __table_args__ = (
        UniqueConstraint('Document_ID' ,'Ontology_ID', 'Encoding_ID', 'Language_ID'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Document_ID = create_fk('docs.tblDocument.ID', required=True)
    Ontology_ID = create_fk('vocab.tblDocumentOntology.ID', required=True)
    Encoding_ID = create_fk('vocab.tblDocumentEncoding.ID', required=True)
    Language_ID = create_fk('vocab.tblDocumentLanguage.ID', required=True)

    # Field set.
    Representation = Column(Text, nullable=False)


class DocumentSubDocument(Entity):
    """Encapsulates document to sub-document relationship information.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentSubDocument'
    __table_args__ = (
        UniqueConstraint('Document_ID' ,'SubDocument_ID'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Document_ID = create_fk('docs.tblDocument.ID', required=True)
    SubDocument_ID = create_fk('docs.tblDocument.ID', required=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: str(instance.Document_ID) + " :: " + str(instance.SubDocument_ID)


class DocumentSummary(Entity):
    """Encapsulates document summary information.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblDocumentSummary'
    __table_args__ = (
        UniqueConstraint('Document_ID' ,'Language_ID'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Document_ID = create_fk('docs.tblDocument.ID', required=True)
    Language_ID = create_fk('vocab.tblDocumentLanguage.ID', required=True)

    # Field set.
    Field_01 = Column(Unicode(1023))
    Field_02 = Column(Unicode(1023))
    Field_03 = Column(Unicode(1023))
    Field_04 = Column(Unicode(1023))
    Field_05 = Column(Unicode(1023))
    Field_06 = Column(Unicode(1023))
    Field_07 = Column(Unicode(1023))
    Field_08 = Column(Unicode(1023))


    @property
    def FieldsConcatanation(self):
        """Gets the concantation of all fields.

        """
        fields = [getattr(self, 'Field_0' + str(i)) for i in range(8) if i is not None]

        return reduce(lambda x, y: x + y, fields, '')


    def as_dict(self):
        """Returns a dictionary representation.

        """
        d = super(DocumentSummary, self).as_dict()

        d['Document'] = self.Document.as_dict()

        return d


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Field_01

