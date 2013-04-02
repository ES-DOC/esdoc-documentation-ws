"""Populates collection of supported projects.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.document_schema import DocumentSchema
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS

# Module exports.
__all__ = ['populate_document_schema']


def populate_document_schema():
    """Populates collection of cim document schemas.

    Keyword Arguments:
    session - db sesssion.
    """
    for version in CIM_SCHEMAS:
        # Create.
        ds = DocumentSchema()
        ds.Version = version


