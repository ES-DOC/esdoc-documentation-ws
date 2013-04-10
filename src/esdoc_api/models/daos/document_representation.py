"""
.. module:: esdoc_api.models.search.document_representation.py
   :copyright: Copyright "Apr 3, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates set of data access operations over a DocumentRepresentation entity.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.models.entities.document import Document
from esdoc_api.models.entities.document_encoding import DocumentEncoding
from esdoc_api.models.entities.document_language import DocumentLanguage
from esdoc_api.models.entities.document_representation import DocumentRepresentation
from esdoc_api.models.entities.document_schema import DocumentSchema


def assign(document, schema, encoding, language, representation):
    """Assigns a representation to a document.

    :param document: The document to which a representation is being assigned.
    :type document: esdoc_api.models.entities.document.Document

    :param schema: Document representation schema.
    :type schema: esdoc_api.models.entities.document_schema.DocumentSchema

    :param encoding: Document representation encoding.
    :type encoding: esdoc_api.models.entities.document_encoding.DocumentEncoding

    :param language: Document representation language.
    :type language: esdoc_api.models.entities.document_language.DocumentLanguage

    :param representation: Document representation, e.g. json | xml.
    :type representation: unicode

    :returns: A document representation.
    :rtype: esdoc_api.models.entities.document_representation.DocumentRepresentation

    """
    # Update or create as appropriate.
    dr = retrieve(document, schema, encoding, language)
    if dr is None:
        dr = DocumentRepresentation()
        dr.Document_ID = document.ID
        dr.Schema_ID = schema.ID
        dr.Encoding_ID = encoding.ID
        dr.Language_ID = language.ID
    dr.Representation = representation

    return dr


def retrieve(document, schema, encoding, language):
    """Retrieves a document representation.

    :param document: A document for which a representation is being retrieved.
    :type document: esdoc_api.models.entities.document.Document

    :param schema: Document representation schema.
    :type schema: esdoc_api.models.entities.document_schema.DocumentSchema

    :param encoding: Document representation encoding.
    :type encoding: esdoc_api.models.entities.document_encoding.DocumentEncoding

    :param language: Document representation language.
    :type language: esdoc_api.models.entities.document_language.DocumentLanguage

    :returns: A document representation.
    :rtype: esdoc_api.models.entities.document_representation.DocumentRepresentation

    """
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
    q = DocumentRepresentation.query
    q = q.filter(DocumentRepresentation.Document_ID==document.ID)
    q = q.filter(DocumentRepresentation.Schema_ID==schema.ID)
    q = q.filter(DocumentRepresentation.Encoding_ID==encoding.ID)
    q = q.filter(DocumentRepresentation.Language_ID==language.ID)

    # Return first.
    return q.first()


def load(document, schema, encoding, language):
    """Loads a document representation.

    :param document: A document for which a representation is being retrieved.
    :type document: esdoc_api.models.entities.document.Document

    :param schema: Associated document schema.
    :type schema: esdoc_api.models.entities.document.Document

    :param encoding: Associated document encoding.
    :type encoding: esdoc_api.models.entities.document.Document

    :param language: Associated document language.
    :type language: esdoc_api.models.entities.document.Document

    :returns: A document representation.
    :rtype: esdoc_api.models.entities.document_representation.DocumentRepresentation

    """
    dr = retrieve(document, schema, encoding, language)

    return None if dr is None else dr.Representation


@classmethod
def remove_all(document):
    """Deletes all document representations.

    :param document: A document for which all representations are being deleted.
    :type document: esdoc_api.models.entities.document.Document

    """
    from esdoc_api.models.entities.document import Document

    # Defensive programming.
    if isinstance(document, Document) == False:
        raise TypeError('document')

    # Set query.
    q = DocumentRepresentation.query
    q = q.filter(DocumentRepresentation.Document_ID==document.ID)

    # Delete all.
    for dr in q.all():
        dr.delete()
