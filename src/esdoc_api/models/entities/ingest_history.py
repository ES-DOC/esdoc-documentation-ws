"""
An operations entity within the Metafor system.
"""

# Module imports.
from elixir import *

from esdoc_api.models.core.entity_base import *
from esdoc_api.models.entities.ingest_state import IngestState


class IngestHistory(CIMEntity):
    """
    An ingest history record.
    """
    # Elixir directives.
    using_options(tablename='tblIngestHistory')
    using_table_options(schema=DB_SCHEMA_INGEST)
    
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
        """
        Gets default sort key.
        """
        self.State = IngestState.get_by_name(state_name)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.StartDateTime
