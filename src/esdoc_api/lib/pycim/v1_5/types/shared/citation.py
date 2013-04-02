"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.533975.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference



# Module exports.
__all__ = ['Citation']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.533975$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Citation(object):
    """A concrete class within the cim v1.5 type system.

    An academic reference to published work.
    """

    def __init__(self):
        """Constructor"""
        super(Citation, self).__init__()
        self.alternative_title = str()               # type = str
        self.collective_title = str()                # type = str
        self.date = datetime.datetime.now()          # type = datetime.datetime
        self.date_type = str()                       # type = str
        self.location = str()                        # type = str
        self.organisation = str()                    # type = str
        self.reference = None                        # type = shared.CimReference
        self.role = str()                            # type = str
        self.title = str()                           # type = str
        self.type = str()                            # type = str


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
        append(d, 'alternative_title', self.alternative_title, False, True, False)
        append(d, 'collective_title', self.collective_title, False, True, False)
        append(d, 'date', self.date, False, True, False)
        append(d, 'date_type', self.date_type, False, True, False)
        append(d, 'location', self.location, False, True, False)
        append(d, 'organisation', self.organisation, False, True, False)
        append(d, 'reference', self.reference, False, False, False)
        append(d, 'role', self.role, False, True, False)
        append(d, 'title', self.title, False, True, False)
        append(d, 'type', self.type, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

