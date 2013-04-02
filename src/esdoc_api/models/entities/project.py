"""An entity within the es-doc api system.

"""

# Module imports.
from elixir import *
from esdoc_api.models.core.entity_base import *


class Project(CIMEntity):
    """A project leveraging the Metafor infrastructure.
    
    """
    # Elixir directives.
    using_options(tablename='tblProject')
    using_table_options(schema=DB_SCHEMA_VOCAB)
    
    # Field set.
    Name =  Field(Unicode(16), required=True, unique=True)
    Description =  Field(Unicode(1023))
    URL =  Field(Unicode(1023))


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Name


    @classmethod
    def retrieve(cls, name):
        """Gets an instance of the entity by code.

        Keyword Arguments:
        name - project name.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name.upper())
