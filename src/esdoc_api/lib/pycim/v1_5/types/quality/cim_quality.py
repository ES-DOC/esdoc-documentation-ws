"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.522416.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo
from esdoc_api.lib.pycim.v1_5.types.quality.report import Report



# Module exports.
__all__ = ['CimQuality']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.522416$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class CimQuality(object):
    """A concrete class within the cim v1.5 type system.

    The starting point for a quality record.  It can contain any number of issues and reports.  An issue is an open-ended description of some issue about a CIM instance.  A record is a prescribed description of some specific quantitative measure that has been applied to a CIM instance.
    """

    def __init__(self):
        """Constructor"""
        super(CimQuality, self).__init__()
        self.cim_info = None                         # type = shared.CimInfo
        self.reports = []                            # type = quality.Report


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
        append(d, 'reports', self.reports, True, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

