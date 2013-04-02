"""
An operations entity within the Metafor system.
"""

# Module imports.
import datetime

from elixir import *

from esdoc_api.models.core.entity_base import *



class IngestURL(CIMEntity):
    """
    A url that has already been ingested.
    """
    # Elixir directives.
    using_options(tablename='tblIngestURL')
    using_table_options(schema=DB_SCHEMA_INGEST)
    
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