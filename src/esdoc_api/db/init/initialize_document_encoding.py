"""
.. module:: initialize_document_encoding.py
   :platform: Unix
   :synopsis: Initializes collection of supported document encodings.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from .. import (
    models, 
    session
    )
import esdoc_api.pyesdoc as pyesdoc



def execute():
    """Initializes collection of supported document encodings.

    """
    for encoding in (pyesdoc.ESDOC_ENCODINGS + pyesdoc.ESDOC_ENCODINGS_CUSTOM):
        # Create.
        i = models.DocumentEncoding()
        i.Encoding = encoding

        # Persist.
        session.insert(i)
