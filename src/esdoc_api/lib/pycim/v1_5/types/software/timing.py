"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.567009.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.software.timing_units import TimingUnits



# Module exports.
__all__ = ['Timing']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.567009$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Timing(object):
    """A concrete class within the cim v1.5 type system.

    Provides information about the rate of couplings and connections and/or the timing characteristics of individual components - for example, the start and stop times that the component was run for or the units of time that a component is able to model (in a single timestep).
    """

    def __init__(self):
        """Constructor"""
        super(Timing, self).__init__()
        self.end = datetime.datetime.now()           # type = datetime.datetime
        self.is_variable_rate = bool()               # type = bool
        self.rate = int()                            # type = int
        self.start = datetime.datetime.now()         # type = datetime.datetime
        self.units = ''                              # type = software.TimingUnits


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
        append(d, 'end', self.end, False, True, False)
        append(d, 'is_variable_rate', self.is_variable_rate, False, True, False)
        append(d, 'rate', self.rate, False, True, False)
        append(d, 'start', self.start, False, True, False)
        append(d, 'units', self.units, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

