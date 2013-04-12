"""An entity within the es-doc api system.

"""

# Module imports.
from elixir import *

from esdoc_api.models.core.entity_base import *



# Set of facet value types.
FACET_VALUE_TYPE_BOOLEAN = u'bool'
FACET_VALUE_TYPE_DATETIME = u'datetime'
FACET_VALUE_TYPE_INTEGER = u'int'
FACET_VALUE_TYPE_STRING = u'str'


# Full set of facet value types.
FACET_VALUE_TYPES = [
    FACET_VALUE_TYPE_BOOLEAN,
    FACET_VALUE_TYPE_DATETIME,
    FACET_VALUE_TYPE_INTEGER,
    FACET_VALUE_TYPE_STRING,
]


# Set of supported types.
EXPERIMENT = "Experiment"
INSTITUTE = "Institute"
MODEL = "Model"
MODEL_COMPONENT = "Model Component"
MODEL_COMPONENT_PROPERTY = "Model Component Property"
MODEL_COMPONENT_PROPERTY_VALUE = "Model Component Property Value"


# Full set of supported types.
FACET_TYPES = [
    EXPERIMENT,
    INSTITUTE,
    MODEL,
    MODEL_COMPONENT,
    MODEL_COMPONENT_PROPERTY,
    MODEL_COMPONENT_PROPERTY_VALUE
]


def get_facet_types():
    """Returns tuple of full set of facets.

    """
    return (
        FacetType.get_by_name(EXPERIMENT),
        FacetType.get_by_name(INSTITUTE),
        FacetType.get_by_name(MODEL),
        FacetType.get_by_name(MODEL_COMPONENT),
        FacetType.get_by_name(MODEL_COMPONENT_PROPERTY),
        FacetType.get_by_name(MODEL_COMPONENT_PROPERTY_VALUE)
    )


# Facet type set indexes.
ID_OF_FACET_EXPERIMENT = 0
ID_OF_FACET_INSTITUTE= 1
ID_OF_FACET_MODEL = 2
ID_OF_FACET_COMPONENT = 3
ID_OF_FACET_PROPERTY = 4
ID_OF_FACET_VALUE = 5


class FacetType(ESDOCEntity):
    """CIM document facet type information.

    """
    # Elixir directives.
    using_options(tablename='tblFacetType')
    using_table_options(schema=DB_SCHEMA_FACETS)

    # Relation set.
    Values = OneToMany('Facet')

    # Field set.
    Name = Field(Unicode(127), required=True, unique=True)
    ValueType = Field(Enum(FACET_VALUE_TYPE_BOOLEAN, \
                           FACET_VALUE_TYPE_DATETIME, \
                           FACET_VALUE_TYPE_INTEGER, \
                           FACET_VALUE_TYPE_STRING, \
                           schema=DB_SCHEMA_VOCAB, name='FacetValueTypeEnum'), \
                      required=True,
                      default=FACET_VALUE_TYPE_STRING)


    def get_value(self, key):
        """Gets an item from sub-collection.

        Keyword Arguments:
        key - facet key.

        """
        for v in self.Values:
            if v.Key.upper() == key[:2047].upper():
                return v
        return None


    @classmethod
    def get_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of facet type.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name)


    @classmethod
    def get_values(cls, name):
        """Gets set of associated values.

        Keyword Arguments:
        name - name of facet type.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        result = []
        for v in cls.get_by(Name=name).Values:
            item = {
                'id' : v.ID,
                'key' : v.Key,
                'value' : v.Value
            }
            if v.KeyForSort:
                item['keyForSort'] = v.KeyForSort
            if v.ValueForDisplay:
                item['valueForDisplay'] = v.ValueForDisplay
            result.append(item)
        return sorted(result, key=lambda v: v['value'])

