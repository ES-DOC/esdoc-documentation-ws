"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.501207.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.activity.simulation import Simulation
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo
from esdoc_api.lib.pycim.v1_5.types.shared.date_range import DateRange
from esdoc_api.lib.pycim.v1_5.types.software.model_component import ModelComponent
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference



# Module exports.
__all__ = ['SimulationRun']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.501207$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class SimulationRun(Simulation):
    """A concrete class within the cim v1.5 type system.

    A SimulationRun is, as the name implies, one single model run. A SimulationRun is a Simulation. There is a one to one association between SimulationRun and (a top-level) SoftwarePackage::ModelComponent.
    """

    def __init__(self):
        """Constructor"""
        super(SimulationRun, self).__init__()
        self.cim_info = None                         # type = shared.CimInfo
        self.date_range = None                       # type = shared.DateRange
        self.model = None                            # type = software.ModelComponent
        self.model_reference = None                  # type = shared.CimReference


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
        d = dict(super(SimulationRun, self).as_dict())
        append(d, 'cim_info', self.cim_info, False, False, False)
        append(d, 'date_range', self.date_range, False, False, False)
        append(d, 'model', self.model, False, False, False)
        append(d, 'model_reference', self.model_reference, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

