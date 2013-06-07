"""
An entity within the Metafor CIM system.
"""

# Module imports.
from esdoc_api.lib.pyesdoc.ontologies.constants import CIM_DEFAULT_LANGUAGE
from elixir import *

from esdoc_api.models.core.entity_base import *
from esdoc_api.lib.pyesdoc.ontologies.constants import *



class DocumentLanguage(ESDOCEntity):
    """
    A language under which a document is published.
    """
    # Elixir directives.
    using_options(tablename='tblDocumentLanguage')
    using_table_options(schema=DB_SCHEMA_VOCAB)
    
    # Field set.
    Code = Field(Unicode(2), required=True)
    Name =  Field(Unicode(127), required=True, unique=True)


    @property
    def FullName(self):
        """
        Gets the full institute name derived by concatanation.
        """
        return self.Code + u" - " + self.Name


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Code


    @classmethod
    def retrieve(cls, code=CIM_DEFAULT_LANGUAGE):
        """Gets an instance of the entity by code.

        Keyword Arguments:
        code - language code.

        """
        # Defensive programming.
        if isinstance(code, str) == False and isinstance(code, unicode) == False:
            raise TypeError('code')

        return cls.get_by(Code=code.lower())

