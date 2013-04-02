"""
An entity within the Metafor CIM system.
"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *
from esdoc_api.models.entities.document_encoding import DocumentEncoding
from esdoc_api.models.entities.document_language import DocumentLanguage
from esdoc_api.models.entities.document_schema import DocumentSchema
from esdoc_api.lib.pycim.core.cim_exception import CIMException


class DocumentRepresentation(CIMEntity):
    """
    A document representation in a supported encoding.
    """
    # Elixir directives.
    using_options(tablename='tblDocumentRepresentation')
    using_table_options(UniqueConstraint('Document_ID', 'Schema_ID',
                                         'Encoding_ID', 'Language_ID'),
                        schema=DB_SCHEMA_DOCS)
    
    # Relation set.
    Document = ManyToOne('Document', required=True)
    Schema = ManyToOne('DocumentSchema', required=True)
    Encoding = ManyToOne('DocumentEncoding', required=True)
    Language = ManyToOne('DocumentLanguage', required=True)

    # Field set.
    Representation = Field(Text)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Encoding


    @classmethod
    def retrieve(cls, document, schema, encoding, language):
        """Gets an instance of the entity by document, schema, encoding & language.

        Keyword Arguments:
        document - associated document.
        schema - associated schema.
        encoding - associated encoding.
        language - associated language.

        """
        from esdoc_api.models.entities.document import Document
        
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if isinstance(schema, DocumentSchema) == False:
            raise TypeError('schema')
        if isinstance(encoding, DocumentEncoding) == False:
            raise TypeError('encoding')
        if isinstance(language, DocumentLanguage) == False:
            raise TypeError('language')

        # Set query.
        q = cls.query
        q = q.filter(cls.Document_ID==document.ID)
        q = q.filter(cls.Schema_ID==schema.ID)
        q = q.filter(cls.Encoding_ID==encoding.ID)
        q = q.filter(cls.Language_ID==language.ID)

        # Return first.
        return q.first()


    @classmethod
    def load(cls, document, schema, encoding, language):
        """Gets an instance of the entity by document, schema, encoding & language.

        Keyword Arguments:
        document - cim document.
        schema - cim schema.
        encoding - document encoding.
        language - document language.

        """
        dr = cls.retrieve(document, schema, encoding, language)

        return None if dr is None else dr.Representation
    

    @classmethod
    def remove_all(cls, document):
        """Deletes all instances of the entity matched by document.

        Keyword Arguments:
        document - associated document.

        """
        from esdoc_api.models.entities.document import Document

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')

        # Set query.
        q = cls.query
        q = q.filter(cls.Document_ID==document.ID)

        # Delete all.
        for dr in q.all():
            dr.delete()


    @classmethod
    def assign(cls, document, schema, encoding, language, representation):
        """Either creates or updates a document representation.

        Keyword Arguments:
        document - cim document.
        schema - cim schema.
        encoding - cim encoding.
        language - language encoding.
        representation - document representation (e.g. json).

        """
        from esdoc_api.models.entities.document import Document
        from esdoc_api.models.entities.document_encoding import DocumentEncoding
        from esdoc_api.models.entities.document_language import DocumentLanguage
        from esdoc_api.models.entities.document_schema import DocumentSchema

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if isinstance(schema, DocumentSchema) == False:
            raise TypeError('schema')
        if isinstance(encoding, DocumentEncoding) == False:
            raise TypeError('encoding')
        if isinstance(language, DocumentLanguage) == False:
            raise TypeError('language')

        # Update or create as appropriate.
        dr = cls.retrieve(document, schema, encoding, language)
        if dr is None:
            dr = DocumentRepresentation()
            dr.Document_ID = document.ID
            dr.Schema_ID = schema.ID
            dr.Encoding_ID = encoding.ID
            dr.Language_ID = language.ID
        dr.Representation = representation

        return dr

