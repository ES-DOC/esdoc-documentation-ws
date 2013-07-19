"""
.. module:: esdoc_api.models.ingest.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The ingestion related set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Unicode
)
from sqlalchemy.orm import relationship

from esdoc_api.models.utils import (
    create_fk,
    Entity
    )



# Module exports.
__all__ = [
    'IngestEndpoint',
    'IngestHistory',
    'IngestURL'
]



# Domain model partition.
_DOMAIN_PARTITION = 'ingest'


class IngestEndpoint(Entity):
    """
    Encapsulates required information in support of an ingestion process.
    """
    # SQLAlchemy directives.
    __tablename__ = 'tblIngestEndpoint'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Institute_ID = create_fk('vocab.tblInstitute.ID')

    # Relationships.
    History = relationship("IngestHistory", backref="Endpoint")

    # Field set.
    Priority =  Column(Integer, nullable=False, default=0)
    Description =  Column(Unicode(63), nullable=False)
    MetadataSource =  Column(Unicode(63))
    IngestorType =  Column(Unicode(15), nullable=False)
    ContactName =  Column(Unicode(128), nullable=False)
    ContactEmail =  Column(Unicode(128), nullable=False)
    ContactTelephone =  Column(Unicode(128), nullable=False)
    IsActive = Column(Boolean, default=False, nullable=False)
    IngestURL =  Column(Unicode(512), nullable=False, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Priority


class IngestHistory(Entity):
    """
    An ingest history record.
    """
    # SQLAlchemy directives.
    __tablename__ = 'tblIngestHistory'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Endpoint_ID = create_fk('ingest.tblIngestEndpoint.ID')
    State_ID = create_fk('vocab.tblIngestState.ID')

    # Field set.
    StartDateTime =  Column(DateTime, nullable=False,
                            default=datetime.datetime.now())
    EndDateTime =  Column(DateTime)
    Count = Column(Integer, default=0)
    TimeInMS = Column(Integer, default=0)
    ErrorMessage = Column(Unicode(1024))


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.StartDateTime


class IngestURL(Entity):
    """
    A url that has already been ingested.
    """
    # SQLAlchemy directives.
    __tablename__ = 'tblIngestURL'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Field set.
    URL =  Column(Unicode(1023), nullable=False, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.URL
