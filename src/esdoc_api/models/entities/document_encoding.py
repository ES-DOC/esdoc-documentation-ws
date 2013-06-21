"""
An entity within the Metafor CIM system.
"""

# Module imports.
from elixir import *

from esdoc_api.models.core.entity_base import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *


class DocumentEncoding(ESDOCEntity):
    """
    A type of supported document encoding.
    """
    # Elixir directives.
    using_options(tablename='tblDocumentEncoding')
    using_table_options(schema=DB_SCHEMA_VOCAB)
    
    # Field set.
    Encoding = Field(Unicode(15), required=True, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Encoding



