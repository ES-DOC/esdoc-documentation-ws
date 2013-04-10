"""
An entity within the Metafor CIM system.
"""

# Module imports.
from esdoc_api.lib.pycim.cim_constants import CIM_DEFAULT_SCHEMA
from esdoc_api.models.entities.document_schema import DocumentSchema


def retrieve(version=CIM_DEFAULT_SCHEMA):
    """Returns a document schema entity.

    :param version: Schema version.
    :type version: str

    :returns: Schema instance.
    :rtype: esdoc_api.models.entities.document_schema.DocumentSchema

    """
    # Defensive programming.
    if version is None:
        raise ValueError('version')

    return DocumentSchema.get_by(Version=version)

