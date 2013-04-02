"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.488432.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.activity.numerical_activity import NumericalActivity
from esdoc_api.lib.pycim.v1_5.types.shared.standard_name import StandardName
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.activity.simulation import Simulation
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference



# Module exports.
__all__ = ['EnsembleMember']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.488432$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class EnsembleMember(NumericalActivity):
    """A concrete class within the cim v1.5 type system.

    A simulation is the implementation of a numerical experiment.  A simulation can be made up of "child" simulations aggregated together to form a "simulation composite".  The "parent" simulation can be made up of whole or partial child simulations, the simulation attributes need to be able to capture this.
    """

    def __init__(self):
        """Constructor"""
        super(EnsembleMember, self).__init__()
        self.ensemble = None                         # type = activity.Ensemble
        self.ensemble_ids = []                       # type = shared.StandardName
        self.ensemble_reference = None               # type = shared.CimReference
        self.simulation = None                       # type = activity.Simulation
        self.simulation_reference = None             # type = shared.CimReference


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
        d = dict(super(EnsembleMember, self).as_dict())
        append(d, 'ensemble', self.ensemble, False, False, False)
        append(d, 'ensemble_ids', self.ensemble_ids, True, False, False)
        append(d, 'ensemble_reference', self.ensemble_reference, False, False, False)
        append(d, 'simulation', self.simulation, False, False, False)
        append(d, 'simulation_reference', self.simulation_reference, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm
from esdoc_api.lib.pycim.v1_5.types.activity.ensemble import Ensemble

