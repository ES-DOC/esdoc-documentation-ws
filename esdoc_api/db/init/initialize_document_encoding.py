# -*- coding: utf-8 -*-
"""
.. module:: initialize_document_encoding.py
   :platform: Unix
   :synopsis: Initializes collection of supported document encodings.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import pyesdoc

from esdoc_api.db import models, session



def execute():
    """Initializes collection of supported document encodings.

    """
    for encoding in (pyesdoc.ENCODINGS + pyesdoc.ENCODINGS_CUSTOM):
        # Create.
        i = models.DocumentEncoding()
        i.encoding = unicode(encoding)

        # Persist.
        session.insert(i)
