"""An entity within the es-doc api system.

"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *


# Module exports.
__all__ = ['Facet']


class Facet(ESDOCEntity):
    """CIM document facet information.

    """
    # Elixir directives.
    using_options(tablename='tblFacet')
    using_table_options(UniqueConstraint('Type_ID' ,'Key'),
    					schema=DB_SCHEMA_FACETS)

    # Relation set.
    Type = ManyToOne('FacetType', required=True)    

    # Field set.
    Key = Field(Unicode(2047), required=True)
    KeyForSort = Field(Unicode(2047))
    Value = Field(Unicode(2047))
    ValueForDisplay = Field(Unicode(2047))
    URL = Field(Unicode(2047))
    

    @classmethod
    def retrieve(cls, type, key):
        """Gets an instance of the entity.

        Keyword Arguments:
        type - facet type.
        key - facet key.

        """
        from esdoc_api.models.entities.facet_type import FacetType

        # Defensive programming.
        if isinstance(type, FacetType) == False:
            raise TypeError('type')
        if key is None:
            raise ValueError('key')

        q = cls.query
        q = q.filter(cls.Type_ID==type.ID)
        q = q.filter(cls.Key==key[:2047])

        return q.first()

    