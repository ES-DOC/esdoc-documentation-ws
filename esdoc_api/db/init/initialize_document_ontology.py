# -*- coding: utf-8 -*-
"""
.. module:: initialize_document_ontology.py
   :platform: Unix
   :synopsis: Initializes collection of supported document ontologies.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import models
from esdoc_api.db import session



def execute():
    """Initializes collection of document ontologies.

    """
    # CIM v1.
    i = models.DocumentOntology()
    i.name = u"cim.1"
    i.version = u"1"
    session.insert(i)

    # CIM v2.
    i = models.DocumentOntology()
    i.name = u"cim.2"
    i.version = u"2"
    session.insert(i)
