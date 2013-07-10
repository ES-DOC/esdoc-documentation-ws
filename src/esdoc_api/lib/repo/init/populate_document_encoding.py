"""
.. module:: esdoc_api.lib.repo.init.populate_document_encoding.py
   :platform: Unix
   :synopsis: Populates collection of supported document encodings.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.models as models

from esdoc_api.lib.pyesdoc.utils.ontologies import ESDOC_ENCODINGS



def populate_document_encoding():
    """Populates collection of supported document encodings.

    """
    for encoding in ESDOC_ENCODINGS:
        # Create.
        i = models.DocumentEncoding()
        i.Encoding = encoding

        # Persist.
        session.insert(i)
