"""An abstract class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.497960.
"""

# Module imports.
import abc
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
import datetime
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.activity.numerical_activity import NumericalActivity
from esdoc_api.lib.pycim.v1_5.types.shared.calendar import Calendar
from esdoc_api.lib.pycim.v1_5.types.activity.conformance import Conformance
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.software.deployment import Deployment
from esdoc_api.lib.pycim.v1_5.types.software.coupling import Coupling
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.data.data_object import DataObject
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.data.data_object import DataObject
from esdoc_api.lib.pycim.v1_5.types.shared.closed_date_range import ClosedDateRange
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference



# Module exports.
__all__ = ['Simulation']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.497960$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Simulation(NumericalActivity):
    """An abstract class within the cim v1.5 type system.

    A simulation is the implementation of a numerical experiment.  A simulation can be made up of "child" simulations aggregated together to form a simulation composite.  The parent simulation can be made up of whole or partial child simulations, the simulation attributes need to be able to capture this.
    """
    # Abstract Base Class module.
    # N.B. - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor"""
        super(Simulation, self).__init__()
        self.authors = str()                         # type = str
        self.calendar = None                         # type = shared.Calendar
        self.conformances = []                       # type = activity.Conformance
        self.control_simulation = None               # type = activity.Simulation
        self.control_simulation_reference = None     # type = shared.CimReference
        self.deployments = []                        # type = software.Deployment
        self.inputs = []                             # type = software.Coupling
        self.output_references = []                  # type = shared.CimReference
        self.outputs = []                            # type = data.DataObject
        self.restart_references = []                 # type = shared.CimReference
        self.restarts = []                           # type = data.DataObject
        self.simulation_id = str()                   # type = str
        self.spinup_date_range = None                # type = shared.ClosedDateRange
        self.spinup_simulation = None                # type = activity.Simulation
        self.spinup_simulation_reference = None      # type = shared.CimReference


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
        d = dict(super(Simulation, self).as_dict())
        append(d, 'authors', self.authors, False, True, False)
        append(d, 'calendar', self.calendar, False, False, False)
        append(d, 'conformances', self.conformances, True, False, False)
        append(d, 'control_simulation', self.control_simulation, False, False, False)
        append(d, 'control_simulation_reference', self.control_simulation_reference, False, False, False)
        append(d, 'deployments', self.deployments, True, False, False)
        append(d, 'inputs', self.inputs, True, False, False)
        append(d, 'output_references', self.output_references, True, False, False)
        append(d, 'outputs', self.outputs, True, False, False)
        append(d, 'restart_references', self.restart_references, True, False, False)
        append(d, 'restarts', self.restarts, True, False, False)
        append(d, 'simulation_id', self.simulation_id, False, True, False)
        append(d, 'spinup_date_range', self.spinup_date_range, False, False, False)
        append(d, 'spinup_simulation', self.spinup_simulation, False, False, False)
        append(d, 'spinup_simulation_reference', self.spinup_simulation_reference, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

