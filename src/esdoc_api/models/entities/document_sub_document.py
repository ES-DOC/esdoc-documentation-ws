"""
An entity within the es-doc api system.
"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *
from esdoc_api.lib.pycim.cim_constants import *

# Module exports.
__all__ = ['DocumentSubDocument']


class DocumentSubDocument(ESDOCEntity):
    """
    A cim document.
    """
    # Elixir directives.
    using_options(tablename='tblDocumentSubDocument')
    using_table_options(UniqueConstraint('Parent_ID' ,'Child_ID'),
                        schema=DB_SCHEMA_DOCS)

    # Relation set.
    Parent = ManyToOne('Document', required=True, lazy=None)
    Child  = ManyToOne('Document', required=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: str(instance.Parent_ID) + " :: " + str(instance.Child_ID)


    @classmethod
    def retrieve(cls, parent):
        """Retrieves a set of instances.

        Keyword Arguments:

        parent - parent document.

        """
        from esdoc_api.models.entities.document import Document

        # Defensive programming.
        if isinstance(parent, Document) == False:
            raise TypeError('parent')

        # Set query.
        q = cls.query
        q = q.filter(cls.Parent_ID==parent.ID)

        # Return first.
        return q.all()


    @classmethod
    def retrieve_duplicate(cls, parent, child):
        """Retrieves a duplicate instance.

        Keyword Arguments:

        parent - parent document.
        child - child document.

        """
        from esdoc_api.models.entities.document import Document

        # Defensive programming.
        if isinstance(parent, Document) == False:
            raise TypeError('parent')
        if isinstance(child, Document) == False:
            raise TypeError('child')

        # Set query.
        q = cls.query
        q = q.filter(cls.Parent_ID==parent.ID)
        q = q.filter(cls.Child_ID==child.ID)

        # Return first.
        return q.first()


    @classmethod
    def create(cls, parent, child):
        """Factory method to create and return an instance.

        Keyword Arguments:

        parent - parent document.
        child - child document.

        """
        from esdoc_api.models.entities.document import Document

        # Defensive programming.
        if isinstance(parent, Document) == False:
            raise TypeError('parent')
        if isinstance(child, Document) == False:
            raise TypeError('child')

        # Instantiate & assign attributes.
        instance = cls.retrieve_duplicate(parent, child)
        if instance is None:
            instance = cls()
            instance.Parent_ID = parent.ID
            instance.Child_ID = child.ID
            parent.HasChildren = True

        return instance

