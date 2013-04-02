"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.553983.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.data_source import DataSource
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.software.connection_property import ConnectionProperty



# Module exports.
__all__ = ['ConnectionEndpoint']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.553983$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class ConnectionEndpoint(object):
    """A concrete class within the cim v1.5 type system.

    The source/target of a coupling.  This is a DataSource (a SoftwareComponent or DataObject).  This is a separate class in order to associate an instanceID with the DataSource; this is used to identify which particular instance is being coupled in case the same DataSource is used more than once in a coupled model (this may be required for BFG).
    """

    def __init__(self):
        """Constructor"""
        super(ConnectionEndpoint, self).__init__()
        self.data_source = None                      # type = shared.DataSource
        self.data_source_reference = None            # type = shared.CimReference
        self.instance_id = str()                     # type = str
        self.properties = []                         # type = software.ConnectionProperty


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
        append(d, 'data_source', self.data_source, False, False, False)
        append(d, 'data_source_reference', self.data_source_reference, False, False, False)
        append(d, 'instance_id', self.instance_id, False, True, False)
        append(d, 'properties', self.properties, True, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

