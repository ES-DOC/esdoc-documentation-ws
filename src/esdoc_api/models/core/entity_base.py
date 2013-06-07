"""
Encapsulates common functionailty available to all Prodiguer entities.
"""

# Module imports.
import datetime

from elixir import *

from esdoc_api.models.core.entity_convertor import EntityConvertor


# PostGres DB Schemas to which the entities are attached.
DB_SCHEMA_DOCS = 'docs'
DB_SCHEMA_INGEST = 'ingest'
DB_SCHEMA_VOCAB = 'vocab'
DB_SCHEMA_FACETS = 'facets'


class ESDOCEntity(Entity):
    """
    A base entity encapsulating common aspects of CIM related entities.
    """
    # Elixir directives.
    using_options(abstract=True)
    using_options_defaults(shortnames=False, auto_primarykey='ID')


    def __repr__(self):
        """
        Returns a string represantation for use in debugging scenarios.
        """
        return EntityConvertor.to_string(self)
    

    def as_dict(self):
        """
        Returns a nested dict/list structure from an entity instance.

        This placeholder allows sub-classes to specify dictionary depth.
        """
        return self.to_dict()


    @property
    def is_new(self):
        """
        Returns a flag indicating whether the entity instance is new or not.
        """
        return True if self.ID is None else False


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.ID
          

    @classmethod
    def get_by_id(cls, id):
        """
        Gets entity instance by id.
        """
        return cls.get_by(ID=id)


    @classmethod
    def get_by_name(cls, name):
        """Gets entity instance by name.
        
        """
        return cls.get_by(Name=name)


    @classmethod
    def get_sorted(cls, collection, sort_key=None):
        """
        Gets sorted collection of instances.
        """
        if sort_key is None:
            sort_key = cls.get_default_sort_key()
        return sorted(collection, key=sort_key, reverse=True)


    @classmethod
    def retrieve_all(cls, sort_key=None):
        """
        Retrieves all entity instances.
        """
        return cls.get_sorted(cls.query.all(), sort_key)


    @classmethod
    def get_all(cls, sort_key=None):
        """
        Gets all entity instances.
        """
        return cls.get_sorted(cls.query.all(), sort_key)


    @classmethod
    def get_count(cls):
        """
        Gets count of entity instances.
        """
        return cls.query.count()


    @classmethod
    def delete_by_id(cls, id):
        """
        Delete entity instance by id.
        """
        cls.delete(ID=id)
