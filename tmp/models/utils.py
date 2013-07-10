"""
.. module:: esdoc_api.lib.repo.models.utils.py
   :copyright: Copyright "Jun 30, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Utility classes / functions used across models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import datetime
import json

from elixir import *



class ESDOCEntity(Entity):
    """Encapsulates common aspects of ESDOC API models.

    """
    # Elixir directives.
    using_options(abstract=True)
    using_options_defaults(shortnames=False, auto_primarykey='ID')


    def __init__(self):
        """Constructor.

        """
        super(ESDOCEntity, self).__init__()


    def __repr__(self):
        """Debugging representation.
        
        """
        return self.as_string()


    def as_dict(self):
        """Returns a nested dict/list structure from an entity instance.

        This placeholder allows sub-classes to specify dictionary depth.
        
        """
        return self.to_dict()


    def as_json(self):
        """Returns a json representation.

        """
        return EntityConvertor.to_json(self)


    def as_string(self):
        """Returns a string representation.

        """
        return EntityConvertor.to_string(self)


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


class JSONEncoder(json.JSONEncoder):
    """Extends standard json encoding so as to handle specific types.

    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat().replace('T', ' ')
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)


class EntityConvertor(object):
    """Encapsulates all entity conversion functions.

    """
    @staticmethod
    def to_dict(target):
        """Returns a dictionary representation.

        """
        result = None
        iterator = None

        # Determine if target is a sequence.
        try:
            iterator = iter(target)
        except TypeError:
            pass

        # Convert.
        if iterator is None:
            result = target.as_dict()
        else:
            result = []
            for item in iterator:
                result.append(item.as_dict())

        return result


    @staticmethod
    def to_json(target):
        """Returns a json representation.

        """
        return unicode(JSONEncoder().encode(EntityConvertor.to_dict(target)))


    @staticmethod
    def to_string(target):
        """Returns a string representation.

        """
        return str(EntityConvertor.to_json(target))

