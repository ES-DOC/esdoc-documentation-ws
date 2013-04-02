"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.487392.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.activity.numerical_activity import NumericalActivity
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo
from esdoc_api.lib.pycim.v1_5.types.activity.ensemble_type import EnsembleType



# Module exports.
__all__ = ['Ensemble']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.487392$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Ensemble(NumericalActivity):
    """A concrete class within the cim v1.5 type system.

    An ensemble is made up of two or more simulations which are to be compared against each other to create ensemble statistics. Ensemble members can differ in terms of initial conditions, physical parameterisation and the model used. An ensemble bundles together sets of ensembleMembers, all of which reference the same Simulation(Run) and include one or more changes.
    """

    def __init__(self):
        """Constructor"""
        super(Ensemble, self).__init__()
        self.cim_info = None                         # type = shared.CimInfo
        self.members = []                            # type = activity.EnsembleMember
        self.types = []                              # type = activity.EnsembleType


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
        d = dict(super(Ensemble, self).as_dict())
        append(d, 'cim_info', self.cim_info, False, False, False)
        append(d, 'members', self.members, True, False, False)
        append(d, 'types', self.types, True, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm
from esdoc_api.lib.pycim.v1_5.types.activity.ensemble_member import EnsembleMember

