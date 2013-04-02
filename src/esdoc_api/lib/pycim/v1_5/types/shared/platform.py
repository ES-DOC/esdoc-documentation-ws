"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.542011.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo
from esdoc_api.lib.pycim.v1_5.types.shared.responsible_party import ResponsibleParty
from esdoc_api.lib.pycim.v1_5.types.shared.machine_compiler_unit import MachineCompilerUnit



# Module exports.
__all__ = ['Platform']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.542011$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Platform(object):
    """A concrete class within the cim v1.5 type system.

    A platform is a description of resources used to deploy a component/simulation.  A platform pairs a machine with a (set of) compilers.  There is also a point of contact for the platform.
    """

    def __init__(self):
        """Constructor"""
        super(Platform, self).__init__()
        self.cim_info = None                         # type = shared.CimInfo
        self.contacts = []                           # type = shared.ResponsibleParty
        self.description = str()                     # type = str
        self.long_name = str()                       # type = str
        self.short_name = str()                      # type = str
        self.units = []                              # type = shared.MachineCompilerUnit


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
        append(d, 'cim_info', self.cim_info, False, False, False)
        append(d, 'contacts', self.contacts, True, False, False)
        append(d, 'description', self.description, False, True, False)
        append(d, 'long_name', self.long_name, False, True, False)
        append(d, 'short_name', self.short_name, False, True, False)
        append(d, 'units', self.units, True, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

