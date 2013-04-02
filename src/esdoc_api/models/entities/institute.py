"""
An operations entity within the Metafor system.
"""

# Module imports.
from elixir import *
from esdoc_api.models.core.entity_base import *


class Institute(CIMEntity):
    """
    An institute leveraging the Metafor infrastructure.
    """
    # Elixir directives.
    using_options(tablename='tblInstitute')
    using_table_options(schema=DB_SCHEMA_VOCAB)
    
    # Field set.
    Name =  Field(Unicode(16), required=True, unique=True)
    Synonym =  Field(Unicode(16), required=False, unique=True)
    LongName =  Field(Unicode(512), required=True)
    CountryCode = Field(Unicode(2), required=True)
    URL =  Field(Unicode(256))


    @property
    def FullName(self):
        """Gets the full institute name derived by concatanation.
        
        """
        return self.CountryCode + u" - " + self.Name + u" - " + self.LongName


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.FullName


    @classmethod
    def get_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of institute.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name)


    @classmethod
    def retrieve_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of institute.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name)
