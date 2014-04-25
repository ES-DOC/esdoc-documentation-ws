"""
.. module:: esdoc_api.lib.repo.init.populate_document_encoding.py
   :platform: Unix
   :synopsis: Populates collection of supported document encodings.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.pyesdoc as pyesdoc
import esdoc_api.lib.repo.session as session
import esdoc_api.models as models



def populate_document_encoding():
    """Populates collection of supported document encodings.

    """
    for encoding in (pyesdoc.ESDOC_ENCODINGS + pyesdoc.ESDOC_ENCODINGS_CUSTOM):
        # Create.
        i = models.DocumentEncoding()
        i.Encoding = encoding

        # Persist.
        session.insert(i)
