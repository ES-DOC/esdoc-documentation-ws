"""
An entity within the Metafor CIM system.
"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *


class DocumentRepresentation(ESDOCEntity):
    """
    A document representation in a supported encoding.
    """
    # Elixir directives.
    using_options(tablename='tblDocumentRepresentation')
    using_table_options(UniqueConstraint('Document_ID', 'Schema_ID',
                                         'Encoding_ID', 'Language_ID'),
                        schema=DB_SCHEMA_DOCS)
    
    # Relation set.
    Document = ManyToOne('Document', required=True)
    Schema = ManyToOne('DocumentSchema', required=True)
    Encoding = ManyToOne('DocumentEncoding', required=True)
    Language = ManyToOne('DocumentLanguage', required=True)

    # Field set.
    Representation = Field(Text)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Encoding


