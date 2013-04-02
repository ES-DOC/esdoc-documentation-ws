"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.517791.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo
from esdoc_api.lib.pycim.v1_5.types.grids.grid_mosaic import GridMosaic



# Module exports.
__all__ = ['GridSpec']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.517791$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class GridSpec(object):
    """A concrete class within the cim v1.5 type system.

    This is a container class for GridSpec objects. A GridSpec object can contain one or more esmModelGrid objects, and one or more esmExchangeGrid objects. These objects may be serialised to one or possibly several files according to taste. Since GridSpec is sub-typed from GML's AbstractGeometryType it can, and should, be identified using a gml:id attribute.
    """

    def __init__(self):
        """Constructor"""
        super(GridSpec, self).__init__()
        self.cim_info = None                         # type = shared.CimInfo
        self.esm_exchange_grids = []                 # type = grids.GridMosaic
        self.esm_model_grids = []                    # type = grids.GridMosaic


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
        append(d, 'cim_info', self.cim_info, False, False, False)
        append(d, 'esm_exchange_grids', self.esm_exchange_grids, True, False, False)
        append(d, 'esm_model_grids', self.esm_model_grids, True, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

