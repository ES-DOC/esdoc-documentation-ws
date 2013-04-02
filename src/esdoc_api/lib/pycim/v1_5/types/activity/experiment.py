"""An abstract class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.489511.
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
from esdoc_api.lib.pycim.v1_5.types.activity.activity import Activity
from esdoc_api.lib.pycim.v1_5.types.activity.measurement_campaign import MeasurementCampaign
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference



# Module exports.
__all__ = ['Experiment']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.489511$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Experiment(Activity):
    """An abstract class within the cim v1.5 type system.

    An experiment might be an activity which is both observational and numerical in focus, for example, a measurement campaign and numerical experiments for an alpine experiment.  It is a place for the scientific description of the reason why an experiment was made.
    """
    # Abstract Base Class module.
    # N.B. - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor"""
        super(Experiment, self).__init__()
        self.generates = []                          # type = str
        self.measurement_campaigns = []              # type = activity.MeasurementCampaign
        self.requires = []                           # type = activity.NumericalActivity
        self.requires_references = []                # type = shared.CimReference
        self.supports = []                           # type = str
        self.supports_references = []                # type = shared.CimReference


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
        d = dict(super(Experiment, self).as_dict())
        append(d, 'generates', self.generates, True, True, False)
        append(d, 'measurement_campaigns', self.measurement_campaigns, True, False, False)
        append(d, 'requires', self.requires, True, False, False)
        append(d, 'requires_references', self.requires_references, True, False, False)
        append(d, 'supports', self.supports, True, True, False)
        append(d, 'supports_references', self.supports_references, True, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm
from esdoc_api.lib.pycim.v1_5.types.activity.numerical_activity import NumericalActivity

