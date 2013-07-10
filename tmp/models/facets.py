"""
.. module:: esdoc_api.lib.repo.models.facets.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The facets set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from sqlalchemy import UniqueConstraint
from elixir import *

from esdoc_api.lib.pyesdoc.utils.ontologies import *
from esdoc_api.lib.repo.models.utils import *



# Module exports.
__all__ = [
    'FACET_VALUE_TYPES',
    'FACET_VALUE_TYPE_BOOLEAN',
    'FACET_VALUE_TYPE_DATETIME',
    'FACET_VALUE_TYPE_INTEGER',
    'FACET_VALUE_TYPE_STRING',
    'FACET_TYPES',
    'EXPERIMENT',
    'INSTITUTE',
    'MODEL',
    'MODEL_COMPONENT',
    'MODEL_COMPONENT_PROPERTY',
    'MODEL_COMPONENT_PROPERTY_VALUE',
    'ID_OF_FACET_EXPERIMENT',
    'ID_OF_FACET_INSTITUTE',
    'ID_OF_FACET_MODEL',
    'ID_OF_FACET_COMPONENT',
    'ID_OF_FACET_PROPERTY', 
    'ID_OF_FACET_VALUE',
    'FACET_RELATIONS',
    'MODEL_2_EXPERIMENT',
    'MODEL_2_INSTITUTE',
    'MODEL_2_COMPONENT',
    'MODEL_2_PROPERTY',
    'MODEL_2_VALUE',
    'COMPONENT_2_COMPONENT',
    'COMPONENT_2_PROPERTY',
    'PROPERTY_2_PROPERTY',
    'PROPERTY_2_VALUE',
    'ID_OF_FACET_RELATION_FROM_COMPONENT_2_COMPONENT',
    'ID_OF_FACET_RELATION_FROM_COMPONENT_2_PROPERTY',
    'ID_OF_FACET_RELATION_FROM_MODEL_2_COMPONENT',
    'ID_OF_FACET_RELATION_FROM_MODEL_2_EXPERIMENT',
    'ID_OF_FACET_RELATION_FROM_MODEL_2_INSTITUTE',
    'ID_OF_FACET_RELATION_FROM_MODEL_2_PROPERTY',
    'ID_OF_FACET_RELATION_FROM_MODEL_2_VALUE',
    'ID_OF_FACET_RELATION_FROM_PROPERTY_2_PROPERTY',
    'ID_OF_FACET_RELATION_FROM_PROPERTY_2_VALUE',
    'get_facet_types',
    'get_facet_relation_types',
    'Facet',
    'FacetRelation',
    'FacetRelationType',
    'FacetType'
]

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

# Set of supported relations.
MODEL_2_EXPERIMENT = "MODEL_2_EXPERIMENT"
MODEL_2_INSTITUTE = "MODEL_2_INSTITUTE"
MODEL_2_COMPONENT = "MODEL_2_COMPONENT"
MODEL_2_PROPERTY = "MODEL_2_PROPERTY"
MODEL_2_VALUE = "MODEL_2_VALUE"
COMPONENT_2_COMPONENT = "COMPONENT_2_COMPONENT"
COMPONENT_2_PROPERTY = "COMPONENT_2_PROPERTY"
PROPERTY_2_PROPERTY = "PROPERTY_2_PROPERTY"
PROPERTY_2_VALUE = "PROPERTY_2_VALUE"

# Full set of supported relations.
FACET_RELATIONS = [
    MODEL_2_EXPERIMENT,
    MODEL_2_INSTITUTE,
    MODEL_2_COMPONENT,
    MODEL_2_PROPERTY,
    MODEL_2_VALUE,
    COMPONENT_2_COMPONENT,
    COMPONENT_2_PROPERTY,
    PROPERTY_2_PROPERTY,
    PROPERTY_2_VALUE
]

def get_facet_relation_types():
    """Returns tuple of full set of facet relations.

    """
    return (
        FacetRelationType.get_by_name(COMPONENT_2_COMPONENT),
        FacetRelationType.get_by_name(COMPONENT_2_PROPERTY),
        FacetRelationType.get_by_name(MODEL_2_COMPONENT),
        FacetRelationType.get_by_name(MODEL_2_EXPERIMENT),
        FacetRelationType.get_by_name(MODEL_2_INSTITUTE),
        FacetRelationType.get_by_name(MODEL_2_PROPERTY),
        FacetRelationType.get_by_name(MODEL_2_VALUE),
        FacetRelationType.get_by_name(PROPERTY_2_PROPERTY),
        FacetRelationType.get_by_name(PROPERTY_2_VALUE)
    )


# Facet type set indexes.
ID_OF_FACET_RELATION_FROM_COMPONENT_2_COMPONENT = 0
ID_OF_FACET_RELATION_FROM_COMPONENT_2_PROPERTY = 1
ID_OF_FACET_RELATION_FROM_MODEL_2_COMPONENT = 2
ID_OF_FACET_RELATION_FROM_MODEL_2_EXPERIMENT = 3
ID_OF_FACET_RELATION_FROM_MODEL_2_INSTITUTE = 4
ID_OF_FACET_RELATION_FROM_MODEL_2_PROPERTY = 5
ID_OF_FACET_RELATION_FROM_MODEL_2_VALUE = 6
ID_OF_FACET_RELATION_FROM_PROPERTY_2_PROPERTY = 7
ID_OF_FACET_RELATION_FROM_PROPERTY_2_VALUE = 8


# Domain model partition.
_DOMAIN_PARTITION = 'facets'


class Facet(ESDOCEntity):
    """A facet mapped from a document attribute.

    """
    # Elixir directives.
    using_options(tablename='tblFacet')
    using_table_options(UniqueConstraint('Type_ID' ,'Key'),
    					schema=_DOMAIN_PARTITION)

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
        # Defensive programming.
        if isinstance(type, FacetType) == False:
            raise TypeError('type')
        if key is None:
            raise ValueError('key')

        q = cls.query
        q = q.filter(cls.Type_ID==type.ID)
        q = q.filter(cls.Key==key[:2047])

        return q.first()


class FacetRelation(ESDOCEntity):
    """The relationship between two facets.

    """
    # Elixir directives.
    using_options(tablename='tblFacetRelation')
    using_table_options(UniqueConstraint('Type_ID', 'From_ID', 'To_ID'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Type = ManyToOne('FacetRelationType', required=True)
    From = ManyToOne('Facet', required=True)
    To = ManyToOne('Facet', required=True)


    @classmethod
    def retrieve(cls, relation_type, from_facet, to_facet):
        """Gets an instance of the entity.

        Keyword Arguments:
        type - relation type.
        from - from facet value.
        to - to facet value.

        """
        # Defensive programming.
        if relation_type is None:
            raise ValueError('relation_type')
        if from_facet is None:
            raise ValueError('from_facet')
        if to_facet is None:
            raise ValueError('to_facet')


        q = cls.query
        q = q.filter(cls.Type_ID==relation_type.ID)
        q = q.filter(cls.From_ID==from_facet.ID)
        q = q.filter(cls.To_ID==to_facet.ID)

        return q.first()


class FacetRelationType(ESDOCEntity):
    """The type of facet relation being indexed, e.g. from a model to a component.

    """
    # Elixir directives.
    using_options(tablename='tblFacetRelationType')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Relation set.
    Relations = OneToMany('FacetRelation')

    # Field set.
    Name = Field(Unicode(127), required=True, unique=True)


    @classmethod
    def get_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of facet relation type.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name)


    @classmethod
    def get_relations(cls, name):
        """Gets set of associated relations.

        Keyword Arguments:
        name - name of facet relations type.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        result = []
        for r in cls.get_by(Name=name).Relations:
            result.append({
                'from' : r.From_ID,
                'to' : r.To_ID
            })
        return sorted(result, key=lambda r: r['from'])


class FacetType(ESDOCEntity):
    """CIM document facet type information.

    """
    # Elixir directives.
    using_options(tablename='tblFacetType')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Relation set.
    Values = OneToMany('Facet')

    # Field set.
    Name = Field(Unicode(127), required=True, unique=True)
    ValueType = Field(Enum(FACET_VALUE_TYPE_BOOLEAN, \
                           FACET_VALUE_TYPE_DATETIME, \
                           FACET_VALUE_TYPE_INTEGER, \
                           FACET_VALUE_TYPE_STRING, \
                           schema=_DOMAIN_PARTITION, name='FacetValueTypeEnum'), \
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
    def get_values(cls, name):
        """Gets set of associated values.

        Keyword Arguments:
        name - name of facet type.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        result = []
        for v in cls.get_by_name(name).Values:
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

