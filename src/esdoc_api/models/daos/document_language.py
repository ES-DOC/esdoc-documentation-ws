"""
An entity within the Metafor CIM system.
"""

# Module imports.
from esdoc_api.lib.pyesdoc.ontologies.constants import CIM_DEFAULT_LANGUAGE
from esdoc_api.models.entities.document_language import DocumentLanguage


def retrieve(code=CIM_DEFAULT_LANGUAGE):
    """Returns a document schema entity.

    :param code: Language code.
    :type code: str

    :returns: Language entity instance.
    :rtype: esdoc_api.models.entities.document_language.DocumentLanguage

    """
    # Defensive programming.
    if not isinstance(code, str) and not isinstance(code, unicode):
        raise TypeError('code')

    return DocumentLanguage.get_by(Code=code.lower())

