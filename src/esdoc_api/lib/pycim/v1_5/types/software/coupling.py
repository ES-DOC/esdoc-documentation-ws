"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.556424.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.software.connection import Connection
from esdoc_api.lib.pycim.v1_5.types.shared.data_source import DataSource
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.software.coupling_property import CouplingProperty
from esdoc_api.lib.pycim.v1_5.types.shared.data_purpose import DataPurpose
from esdoc_api.lib.pycim.v1_5.types.software.coupling_endpoint import CouplingEndpoint
from esdoc_api.lib.pycim.v1_5.types.software.spatial_regridding import SpatialRegridding
from esdoc_api.lib.pycim.v1_5.types.software.time_lag import TimeLag
from esdoc_api.lib.pycim.v1_5.types.software.timing import Timing
from esdoc_api.lib.pycim.v1_5.types.software.time_transformation import TimeTransformation
from esdoc_api.lib.pycim.v1_5.types.software.processor_component import ProcessorComponent
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.software.connection_type import ConnectionType



# Module exports.
__all__ = ['Coupling']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.556424$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Coupling(object):
    """A concrete class within the cim v1.5 type system.

    A coupling represents a set of Connections between a source and target component. Couplings can be complete or incomplete. If they are complete then they must include all Connections between model properties. If they are incomplete then the connections can be underspecified or not listed at all.
    """

    def __init__(self):
        """Constructor"""
        super(Coupling, self).__init__()
        self.connections = []                        # type = software.Connection
        self.description = str()                     # type = str
        self.is_fully_specified = bool()             # type = bool
        self.priming = None                          # type = shared.DataSource
        self.priming_reference = None                # type = shared.CimReference
        self.properties = []                         # type = software.CouplingProperty
        self.purpose = ''                            # type = shared.DataPurpose
        self.sources = []                            # type = software.CouplingEndpoint
        self.spatial_regriddings = []                # type = software.SpatialRegridding
        self.target = None                           # type = software.CouplingEndpoint
        self.time_lag = None                         # type = software.TimeLag
        self.time_profile = None                     # type = software.Timing
        self.time_transformation = None              # type = software.TimeTransformation
        self.transformers = []                       # type = software.ProcessorComponent
        self.transformers_references = []            # type = shared.CimReference
        self.type = ''                               # type = software.ConnectionType


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
        append(d, 'connections', self.connections, True, False, False)
        append(d, 'description', self.description, False, True, False)
        append(d, 'is_fully_specified', self.is_fully_specified, False, True, False)
        append(d, 'priming', self.priming, False, False, False)
        append(d, 'priming_reference', self.priming_reference, False, False, False)
        append(d, 'properties', self.properties, True, False, False)
        append(d, 'purpose', self.purpose, False, False, True)
        append(d, 'sources', self.sources, True, False, False)
        append(d, 'spatial_regriddings', self.spatial_regriddings, True, False, False)
        append(d, 'target', self.target, False, False, False)
        append(d, 'time_lag', self.time_lag, False, False, False)
        append(d, 'time_profile', self.time_profile, False, False, False)
        append(d, 'time_transformation', self.time_transformation, False, False, False)
        append(d, 'transformers', self.transformers, True, False, False)
        append(d, 'transformers_references', self.transformers_references, True, False, False)
        append(d, 'type', self.type, False, False, True)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

