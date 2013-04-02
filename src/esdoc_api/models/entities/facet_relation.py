"""An entity within the es-doc api system.

"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *



class FacetRelation(CIMEntity):
    """CIM document facet relation information.

    """
    # Elixir directives.
    using_options(tablename='tblFacetRelation')
    using_table_options(UniqueConstraint('Type_ID', 'From_ID', 'To_ID'),
                        schema=DB_SCHEMA_FACETS)

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
