"""
.. module:: esdoc_api.lib.repo.init.populate_document_ontology.py
   :platform: Unix
   :synopsis: Populates collection of supported document ontologies.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.session as session
import esdoc_api.models as models
from esdoc_api.lib.utils.string import get_rows



_data = u'''cim.1 | 1'''


def populate_document_ontology():
    """Populates collection of document ontologies.

    """
    for row in get_rows(_data):
        # Create.
        i = models.DocumentOntology()
        i.Name = row[0]
        i.Version = row[1]

        # Persist.
        session.insert(i)
        