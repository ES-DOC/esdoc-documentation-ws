"""Populates collection of supported document categories.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.document_encoding import DocumentEncoding
from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_ENCODINGS




def populate_document_encoding():
    """Populates collection of supported document encodings.

    Keyword Arguments:
    session - db sesssion.
    """
    for encoding in CIM_ENCODINGS:
        # Create.
        e = DocumentEncoding()
        e.Encoding = encoding

