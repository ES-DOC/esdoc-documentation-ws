"""An entity within the es-doc api system.

"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *
from esdoc_api.lib.pycim.cim_constants import *


# Module exports.
__all__ = ['DocumentType']



class DocumentType(CIMEntity):
    """CIM document type information.
    
    """
    # Elixir directives.
    using_options(tablename='tblDocumentType')
    using_table_options(UniqueConstraint('Schema_ID' ,'Package', 'Name'),
                        UniqueConstraint('Schema_ID' ,'ShortName'),
                        schema=DB_SCHEMA_VOCAB)

    # Relation set.
    Schema = ManyToOne('DocumentSchema', required=True)

    # Field set.
    Package = Field(Unicode(63), required=True)
    Name = Field(Unicode(63), required=True)
    ShortName = Field(Unicode(31), required=True)
    DisplayName = Field(Unicode(63), required=True)


    def full_name(self):
        result = self.Schema.Version
        result += '.'
        result = self.Package.strip().lower()
        result += '.'
        result = self.Name.strip().lower()
        return result


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.
        
        """
        return lambda instance: instance.full_name


