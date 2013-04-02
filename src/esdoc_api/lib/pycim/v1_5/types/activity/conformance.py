"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.486540.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.activity.frequency_type import FrequencyType
from esdoc_api.lib.pycim.v1_5.types.activity.numerical_requirement import NumericalRequirement
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.shared.data_source import DataSource
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.activity.conformance_type import ConformanceType



# Module exports.
__all__ = ['Conformance']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.486540$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Conformance(object):
    """A concrete class within the cim v1.5 type system.

    A conformance class maps how a configured model component met a specific numerical requirement.  For example, for a double CO2 boundary condition, a model component might read a CO2 dataset in which CO2 has been doubled, or it might modify a parameterisation (presumably with a factor of two somewhere).  So, the conformance links a requirement to a DataSource (which can be either an actual DataObject or a property of a model component).  In some cases a model/simulation may _naturally_ conform to a requirement.  In this case there would be no reference to a DataSource but the conformant attribute would be true.  If something is purpopsefully non-conformant then the conformant attribute would be false.
    """

    def __init__(self):
        """Constructor"""
        super(Conformance, self).__init__()
        self.description = str()                     # type = str
        self.frequency = ''                          # type = activity.FrequencyType
        self.is_conformant = bool()                  # type = bool
        self.requirements = []                       # type = activity.NumericalRequirement
        self.requirements_references = []            # type = shared.CimReference
        self.sources = []                            # type = shared.DataSource
        self.sources_references = []                 # type = shared.CimReference
        self.type = ''                               # type = activity.ConformanceType


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
        append(d, 'description', self.description, False, True, False)
        append(d, 'frequency', self.frequency, False, False, True)
        append(d, 'is_conformant', self.is_conformant, False, True, False)
        append(d, 'requirements', self.requirements, True, False, False)
        append(d, 'requirements_references', self.requirements_references, True, False, False)
        append(d, 'sources', self.sources, True, False, False)
        append(d, 'sources_references', self.sources_references, True, False, False)
        append(d, 'type', self.type, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

