"""
An entity within the es-doc api system.
"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *

# Module exports.
__all__ = ['DocumentByExternalID']



class DocumentByExternalID(CIMEntity):
    """The external id of a cim document.
    
    """
    # Elixir directives.
    using_options(tablename='tblDocumentByExternalID')
    using_table_options(UniqueConstraint('Project_ID', 'Document_ID', 'ExternalID'),
                        schema=DB_SCHEMA_DOCS)

    # Relation set.
    Project = ManyToOne('Project', required=True)
    Document = ManyToOne('Document', required=True)

    # Field set.
    ExternalID = Field(Unicode(255), required=True)


    @classmethod
    def retrieve(cls, project, external_id, latest_only=True):
        """Retrieves a single instance.

        Keyword Arguments:
        document - a cim document.
        external_id - a cim document.

        """
        from esdoc_api.models.entities.project import Project
        from esdoc_api.models.entities.document import Document

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if external_id is None:
            raise ValueError('external_id')

        # Set query.
        q = cls.query.join(cls.Document)
        q = q.filter(cls.Project_ID==project.ID)
        q = q.filter(cls.ExternalID.like('%' + external_id.upper() + '%'))
        if latest_only == True:
            q = q.filter(Document.IsLatest==True)

        # Return first.
        return q.all()


    @classmethod
    def retrieve_duplicate(cls, document, external_id):
        """Retrieves a duplicate instance.

        Keyword Arguments:
        document - a cim document.
        external_id - a cim document.

        """
        from esdoc_api.models.entities.document import Document

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if external_id is None:
            raise ValueError('external_id')

        # Set query.
        q = cls.query.join(cls.Document)
        q = q.filter(cls.Project_ID==document.Project_ID)
        q = q.filter(cls.Document_ID==document.ID)
        q = q.filter(cls.ExternalID==external_id.upper())

        # Return first.
        return q.first()


    @classmethod
    def create(cls, document, first_only=False):
        """Create & returns external id references to cim documents.

        Keyword Arguments:
        document - a cim document.
        first_only - flag indicating whether only the first external id will be imported.

        """
        from esdoc_api.models.entities.document import Document

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if document.pycim_doc is None:
            raise ValueError('document.pycim_doc')

        collection = []
        for id in document.pycim_doc.cim_info.external_ids:
            instance = cls.retrieve_duplicate(document, id.value)
            if instance is None:
                instance = cls()
                instance.Project_ID = document.Project_ID
                instance.Document_ID = document.ID
                instance.ExternalID = id.value.upper()
            collection.append(instance)
            if first_only:
                break

        return collection