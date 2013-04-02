"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.531494.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.change import Change



# Module exports.
__all__ = ['CimReference']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.531494$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class CimReference(object):
    """A concrete class within the cim v1.5 type system.

    A reference to another cim entity
    """

    def __init__(self):
        """Constructor"""
        super(CimReference, self).__init__()
        self.changes = []                            # type = shared.Change
        self.description = str()                     # type = str
        self.external_id = str()                     # type = str
        self.id = uuid.uuid4()                       # type = uuid.UUID
        self.name = str()                            # type = str
        self.type = str()                            # type = str
        self.version = str()                         # type = str


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
        d = dict()
        append(d, 'changes', self.changes, True, False, False)
        append(d, 'description', self.description, False, True, False)
        append(d, 'external_id', self.external_id, False, True, False)
        append(d, 'id', self.id, False, True, False)
        append(d, 'name', self.name, False, True, False)
        append(d, 'type', self.type, False, True, False)
        append(d, 'version', self.version, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

