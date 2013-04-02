"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.527855.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.cim_relationship import CimRelationship
from esdoc_api.lib.pycim.v1_5.types.shared.cim_document_relationship_target import CimDocumentRelationshipTarget
from esdoc_api.lib.pycim.v1_5.types.shared.cim_document_relationship_type import CimDocumentRelationshipType



# Module exports.
__all__ = ['CimDocumentRelationship']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.527855$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class CimDocumentRelationship(CimRelationship):
    """A concrete class within the cim v1.5 type system.

    Contains the set of relationships supported by a Document.
    """

    def __init__(self):
        """Constructor"""
        super(CimDocumentRelationship, self).__init__()
        self.target = None                           # type = shared.CimDocumentRelationshipTarget
        self.type = ''                               # type = shared.CimDocumentRelationshipType


    def as_dict(self):
        """Gets dictionary representation of self used to create other representations such as json, xml ...etc.

        """
        def append(d, key, value, is_iterative, is_primitive, is_enum):
            if value is None:
                if is_iterative:
                    value = []
            elif is_primitive == False and is_enum == False:
                if is_iterative:
                    value = map(lambda i : i.as_dict(), value)
                else:
                    value = value.as_dict()
            d[key] = value

        # Populate a deep dictionary.
        d = dict(super(CimDocumentRelationship, self).as_dict())
        append(d, 'target', self.target, False, False, False)
        append(d, 'type', self.type, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

