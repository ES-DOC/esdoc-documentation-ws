"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.524670.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.quality.evaluation import Evaluation
from esdoc_api.lib.pycim.v1_5.types.shared.responsible_party import ResponsibleParty
from esdoc_api.lib.pycim.v1_5.types.quality.measure import Measure



# Module exports.
__all__ = ['Report']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.524670$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Report(object):
    """A concrete class within the cim v1.5 type system.

    
    """

    def __init__(self):
        """Constructor"""
        super(Report, self).__init__()
        self.date = datetime.datetime.now()          # type = datetime.datetime
        self.evaluation = None                       # type = quality.Evaluation
        self.evaluator = None                        # type = shared.ResponsibleParty
        self.measure = None                          # type = quality.Measure


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
        append(d, 'date', self.date, False, True, False)
        append(d, 'evaluation', self.evaluation, False, False, False)
        append(d, 'evaluator', self.evaluator, False, False, False)
        append(d, 'measure', self.measure, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

