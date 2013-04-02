"""
A controlled vocabulary entity within the Metafor system.
"""

# Module imports.
from elixir import *
from esdoc_api.models.core.entity_base import *

# Constants pertaining to states.
EXECUTION_STATE_QUEUED = u"QUEUED"
EXECUTION_STATE_RUNNING = u"RUNNING"
EXECUTION_STATE_SUSPENDED = u"SUSPENDED"
EXECUTION_STATE_COMPLETE = u"COMPLETE"
EXECUTION_STATE_ERROR = u"ERROR"


class IngestState(CIMEntity):
    """
    The state that a ingest process may be in, i.e. InProgress, Queued, Error...etc.
    """
    # Elixir directives.
    using_options(tablename='tblIngestState')
    using_table_options(schema=DB_SCHEMA_VOCAB)
    
    # Field set.
    Name =  Field(Unicode(16), required=True, unique=True)
    Description =  Field(Unicode(128), required=True)
    Code =  Field(Integer, required=True, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Code


    @classmethod
    def get_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of ingest state.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')
        
        return cls.get_by(Name=name)
