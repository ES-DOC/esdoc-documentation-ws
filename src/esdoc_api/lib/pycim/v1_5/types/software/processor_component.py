"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.562131.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.software.component import Component
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo



# Module exports.
__all__ = ['ProcessorComponent']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.562131$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class ProcessorComponent(Component):
    """A concrete class within the cim v1.5 type system.

    A ModelComponent is a scientific model; it represents code which models some physical phenomena for a particular length of time.
    """

    def __init__(self):
        """Constructor"""
        super(ProcessorComponent, self).__init__()
        self.cim_info = None                         # type = shared.CimInfo


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
        d = dict(super(ProcessorComponent, self).as_dict())
        append(d, 'cim_info', self.cim_info, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

