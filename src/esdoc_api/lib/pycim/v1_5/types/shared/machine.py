"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.539126.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.interconnect_type import InterconnectType
from esdoc_api.lib.pycim.v1_5.types.shared.operating_system_type import OperatingSystemType
from esdoc_api.lib.pycim.v1_5.types.shared.processor_type import ProcessorType
from esdoc_api.lib.pycim.v1_5.types.shared.machine_type import MachineType
from esdoc_api.lib.pycim.v1_5.types.shared.machine_vendor_type import MachineVendorType



# Module exports.
__all__ = ['Machine']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.539126$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Machine(object):
    """A concrete class within the cim v1.5 type system.

    A description of a machine used by a particular platform
    """

    def __init__(self):
        """Constructor"""
        super(Machine, self).__init__()
        self.cores_per_processor = int()             # type = int
        self.description = str()                     # type = str
        self.interconnect = ''                       # type = shared.InterconnectType
        self.libraries = []                          # type = str
        self.location = str()                        # type = str
        self.maximum_processors = int()              # type = int
        self.name = str()                            # type = str
        self.operating_system = ''                   # type = shared.OperatingSystemType
        self.processor_type = ''                     # type = shared.ProcessorType
        self.system = str()                          # type = str
        self.type = ''                               # type = shared.MachineType
        self.vendor = ''                             # type = shared.MachineVendorType


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
        append(d, 'cores_per_processor', self.cores_per_processor, False, True, False)
        append(d, 'description', self.description, False, True, False)
        append(d, 'interconnect', self.interconnect, False, False, True)
        append(d, 'libraries', self.libraries, True, True, False)
        append(d, 'location', self.location, False, True, False)
        append(d, 'maximum_processors', self.maximum_processors, False, True, False)
        append(d, 'name', self.name, False, True, False)
        append(d, 'operating_system', self.operating_system, False, False, True)
        append(d, 'processor_type', self.processor_type, False, False, True)
        append(d, 'system', self.system, False, True, False)
        append(d, 'type', self.type, False, False, True)
        append(d, 'vendor', self.vendor, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

