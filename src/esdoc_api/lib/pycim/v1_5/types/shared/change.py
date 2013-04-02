"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.526360.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.responsible_party import ResponsibleParty
from esdoc_api.lib.pycim.v1_5.types.shared.change_property import ChangeProperty
from esdoc_api.lib.pycim.v1_5.types.shared.change_property_type import ChangePropertyType



# Module exports.
__all__ = ['Change']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.526360$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Change(object):
    """A concrete class within the cim v1.5 type system.

    A description of [a set of] changes applied at a particular time, by a particular party, to a particular unit of metadata.
    """

    def __init__(self):
        """Constructor"""
        super(Change, self).__init__()
        self.author = None                           # type = shared.ResponsibleParty
        self.date = datetime.datetime.now()          # type = datetime.datetime
        self.description = str()                     # type = str
        self.details = []                            # type = shared.ChangeProperty
        self.name = str()                            # type = str
        self.type = ''                               # type = shared.ChangePropertyType


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
        append(d, 'author', self.author, False, False, False)
        append(d, 'date', self.date, False, True, False)
        append(d, 'description', self.description, False, True, False)
        append(d, 'details', self.details, True, False, False)
        append(d, 'name', self.name, False, True, False)
        append(d, 'type', self.type, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

