"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.560622.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.software.component import Component
from esdoc_api.lib.pycim.v1_5.types.activity.activity import Activity
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo
from esdoc_api.lib.pycim.v1_5.types.software.timing import Timing
from esdoc_api.lib.pycim.v1_5.types.software.model_component_type import ModelComponentType



# Module exports.
__all__ = ['ModelComponent']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.560622$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class ModelComponent(Component):
    """A concrete class within the cim v1.5 type system.

    A ModelComponent is a scientific model; it represents code which models some physical phenomena for a particular length of time.
    """

    def __init__(self):
        """Constructor"""
        super(ModelComponent, self).__init__()
        self.activity = None                         # type = activity.Activity
        self.cim_info = None                         # type = shared.CimInfo
        self.timing = None                           # type = software.Timing
        self.type = ''                               # type = software.ModelComponentType
        self.types = []                              # type = software.ModelComponentType


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
        d = dict(super(ModelComponent, self).as_dict())
        append(d, 'activity', self.activity, False, False, False)
        append(d, 'cim_info', self.cim_info, False, False, False)
        append(d, 'timing', self.timing, False, False, False)
        append(d, 'type', self.type, False, False, True)
        append(d, 'types', self.types, True, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

