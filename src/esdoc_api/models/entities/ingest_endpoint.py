"""
An operations entity within the Metafor system.
"""

# Module imports.
import datetime

from elixir import *

from esdoc_api.models.core.entity_base import *


class IngestEndpoint(ESDOCEntity):
    """
    Encapsulates required information in support of an ingestion process.
    """
    # Elixir directives.
    using_options(tablename='tblIngestEndpoint')
    using_table_options(schema=DB_SCHEMA_INGEST)
    
    # Relation set.
    Institute =  ManyToOne('Institute')
    History = OneToMany('IngestHistory')
    Priority =  Field(Integer, required=True, default=0)

    # Field set.
    Description =  Field(Unicode(63), required=True)
    MetadataSource =  Field(Unicode(63))
    IngestorType =  Field(Unicode(15), required=True)
    ContactName =  Field(Unicode(128), required=True)
    ContactEmail =  Field(Unicode(128), required=True)
    ContactTelephone =  Field(Unicode(128), required=True)
    IsActive = Field(Boolean, default=False, required=True)
    IngestURL =  Field(Unicode(512), required=True, unique=True)

    
    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Institute.Priority


    @classmethod
    def get_active(cls):
        """
        Gets all active ingests registrations.
        """
        return sorted(cls.query.filter(cls.IsActive==True).all(),
                      key=lambda instance: instance.Priority,
                      reverse=True)


    @classmethod
    def retrieve_by_url(cls, url):
        """
        Gets all endpoint by passed url.
        """
        return cls.query.filter(cls.IngestURL==url).first()

    