"""
.. module:: esdoc_api.lib.repo.models.ingest.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The ingestion related set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from elixir import *

from esdoc_api.lib.pyesdoc.utils.ontologies import *
from esdoc_api.lib.repo.models.utils import *



# Module exports.
__all__ = [
    'IngestEndpoint',
    'IngestHistory',
    'IngestURL'
]



# Domain model partition.
_DOMAIN_PARTITION = 'ingest'


class IngestEndpoint(ESDOCEntity):
    """
    Encapsulates required information in support of an ingestion process.
    """
    # Elixir directives.
    using_options(tablename='tblIngestEndpoint')
    using_table_options(schema=_DOMAIN_PARTITION)

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


class IngestHistory(ESDOCEntity):
    """
    An ingest history record.
    """
    # Elixir directives.
    using_options(tablename='tblIngestHistory')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Relation set.
    Endpoint = ManyToOne('IngestEndpoint')
    State = ManyToOne('IngestState')

    # Field set.
    StartDateTime =  Field(DateTime, required=True, default=datetime.datetime.now)
    EndDateTime =  Field(DateTime)
    Count = Field(Integer, default=0)
    TimeInMS = Field(Integer, default=0)
    ErrorMessage = Field(Unicode(1024))


    def set_state(self, state_name):
        """Assigns state by picking up corresponding domain object.
        
        """
        from esdoc_api.lib.repo.models import IngestState
        
        self.State = IngestState.get_by_name(state_name)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.StartDateTime


class IngestURL(ESDOCEntity):
    """
    A url that has already been ingested.
    """
    # Elixir directives.
    using_options(tablename='tblIngestURL')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Field set.
    URL =  Field(Unicode(1023), required=True, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.URL


    @classmethod
    def retrieve(cls, url):
        """
        Gets all endpoint by passed url.
        """
        return cls.query.filter(cls.URL==url).first()


    @classmethod
    def create(cls, url):
        """Factory method to create and return an instance.

        Keyword Arguments:

        url - a url previously ingested.

        """
        # Defensive programming.
        if url is None:
            raise TypeError('url')

        # Instantiate & assign attributes.
        instance = cls()
        instance.URL = url

        return instance