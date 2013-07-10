"""
.. module:: esdoc_api.lib.repo.models.utils.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Domain model utility classes and functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import datetime
import json

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData
    )
from sqlalchemy.ext.declarative import declarative_base



# Module exports.
__all__ = [
    'metadata',
    'create_fk',
    'Entity',
    'EntityConvertor'
]


# Common sqlalchemy metadata container.
metadata = MetaData()



def create_fk(name, required=False):
    """Factory function to return a foreign key

    """
    return Column(Integer, ForeignKey(name), nullable=not required)


class BaseEntity(object):
    """Base entity sub-classed from all Prodiguer models.

    """
    # Entity attributes.
    ID = Column(Integer, primary_key=True)


    def __init__(self):
        """Constructor.

        """
        super(BaseEntity, self).__init__()


    def __repr__(self):
        """Debugging representation.

        """
        return self.as_string()


    def as_dict(self):
        """Returns a dictionary representation.

        """
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

    def as_json(self):
        """Returns a json representation.

        """
        return EntityConvertor.to_json(self)


    def as_string(self):
        """Returns a string representation.

        """
        return EntityConvertor.to_json(self)


    @property
    def is_new(self):
        """Returns a flag indicating whether the entity instance is new or not.

        """
        return True if self.ID is None else False


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.

        """
        if hasattr(cls, 'FullName'):
            return lambda instance: instance.FullName.upper()
        elif hasattr(cls, 'Name'):
            return lambda instance: instance.Name.upper()
        elif hasattr(cls, 'OrdinalPosition'):
            return lambda instance: str(instance.OrdinalPosition)
        else:
            lambda instance: instance.ID


    @classmethod
    def get_sorted(cls, collection, sort_key=None):
        """Gets sorted collection of instances.

        """
        if sort_key is None:
            sort_key=cls.get_default_sort_key()
        return sorted(collection, key=sort_key)



# Mixin with sql alchemy.
Entity = declarative_base(metadata=metadata, cls=BaseEntity)


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
        return str(EntityConvertor.to_dict(target))


