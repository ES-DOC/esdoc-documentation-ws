"""
.. module:: esdoc_api.models.facets.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The facets set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from sqlalchemy import (
    Column,
    Enum,
    Unicode,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from esdoc_api.models.utils import (
    create_fk,
    Entity
    )



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
    'FACET_RELATION_TYPES',
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
# N.B. this order is cross-referenced with order ot ID's.
FACET_RELATION_TYPES = [
    COMPONENT_2_COMPONENT,
    COMPONENT_2_PROPERTY,
    MODEL_2_COMPONENT,
    MODEL_2_EXPERIMENT,
    MODEL_2_INSTITUTE,
    MODEL_2_PROPERTY,
    MODEL_2_VALUE,
    PROPERTY_2_PROPERTY,
    PROPERTY_2_VALUE
]

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


class Facet(Entity):
    """A facet derived from a map/reduce job over a document attribute.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblFacet'
    __table_args__ = (
        UniqueConstraint('Type_ID' ,'Key'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Type_ID = create_fk('facets.tblFacetType.ID', required=True)
    Project_ID = create_fk('vocab.tblProject.ID', required=False)

    # Field set.
    Key = Column(Unicode(2047), nullable=False)
    KeyForSort = Column(Unicode(2047))
    Value = Column(Unicode(2047))
    ValueForDisplay = Column(Unicode(2047))
    URL = Column(Unicode(2047))


class FacetRelation(Entity):
    """The relationship between two facets.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblFacetRelation'
    __table_args__ = (
        UniqueConstraint('Type_ID' ,'From_ID', 'To_ID'),
        {'schema' : _DOMAIN_PARTITION}
    )

    # Foreign keys.
    Type_ID = create_fk('facets.tblFacetRelationType.ID', required=True)
    From_ID = create_fk('facets.tblFacet.ID', required=True)
    To_ID = create_fk('facets.tblFacet.ID', required=True)
    Project_ID = create_fk('vocab.tblProject.ID', required=False)


class FacetRelationType(Entity):
    """The type of facet relation being indexed, e.g. from a model to a component.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblFacetRelationType'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Relationships.
    Relations = relationship("FacetRelation", backref="Type")

    # Field set.
    Name = Column(Unicode(127), nullable=False, unique=True)


# Enumeration over set of facet value types.
FacetValueTypeEnum = Enum(FACET_VALUE_TYPE_BOOLEAN,
                          FACET_VALUE_TYPE_DATETIME, \
                          FACET_VALUE_TYPE_INTEGER, \
                          FACET_VALUE_TYPE_STRING, \
                          schema=_DOMAIN_PARTITION, \
                          name='FacetValueTypeEnum')


class FacetType(Entity):
    """Facet type information.

    """
    # SQLAlchemy directives.
    __tablename__ = 'tblFacetType'
    __table_args__ = (
        {'schema' : _DOMAIN_PARTITION}
    )

    # Relationships.
    Values = relationship("Facet", backref="Type")

    # Field set.
    Name = Column(Unicode(127), nullable=False, unique=True)
    ValueType = Column(FacetValueTypeEnum, nullable=False, default=FACET_VALUE_TYPE_STRING)


    def get_value(self, key):
        """Gets an item from sub-collection.

        Keyword Arguments:
        key - facet key.

        """
        for v in self.Values:
            if v.Key.upper() == key[:2047].upper():
                return v
        return None

