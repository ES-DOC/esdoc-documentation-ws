"""An entity within the es-doc api system.

"""

# Module imports.
from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_DEFAULT_SCHEMA
from elixir import *

from esdoc_api.models.core.entity_base import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *


# Module exports.
__all__ = ['DocumentSchema']



class DocumentSchema(ESDOCEntity):
    """CIM document schema information.
    
    """
    # Elixir directives.
    using_options(tablename='tblDocumentSchema')
    using_table_options(schema=DB_SCHEMA_VOCAB)
    
    # Relation set.
    # TODO Types = OneToMany('DocumentType')

    # Field set.
    Name = Field(Unicode(63), required=True, unique=True)
    Version = Field(Unicode(31), required=True, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.
        
        """
        return lambda instance: instance.Version


    @classmethod
    def retrieve(cls, version=CIM_DEFAULT_SCHEMA):
        """Gets a document schema by version.

        Keyword Arguments:
        version - schema version.

        """
        # Defensive programming.
        if version is None:
            raise ValueError('version')

        return cls.get_by(Version=version)

