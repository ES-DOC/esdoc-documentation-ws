"""Populates collection of supported projects.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.document_schema import DocumentSchema
from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_SCHEMAS



def populate_document_schema():
    """Populates collection of cim document schemas.

    Keyword Arguments:
    session - db sesssion.
    """
    for version in CIM_SCHEMAS:
        # Create.
        ds = DocumentSchema()
        ds.Version = version


