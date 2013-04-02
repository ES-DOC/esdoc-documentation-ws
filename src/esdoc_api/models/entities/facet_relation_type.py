"""An entity within the es-doc api system.

"""

# Module imports.
from elixir import *

from esdoc_api.models.core.entity_base import *



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


class FacetRelationType(CIMEntity):
    """CIM document facet relation type information.

    """
    # Elixir directives.
    using_options(tablename='tblFacetRelationType')
    using_table_options(schema=DB_SCHEMA_FACETS)

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

