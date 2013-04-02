"""An abstract class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.483356.
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
from esdoc_api.lib.pycim.v1_5.types.activity.project_type import ProjectType
from esdoc_api.lib.pycim.v1_5.types.shared.responsible_party import ResponsibleParty



# Module exports.
__all__ = ['Activity']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.483356$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Activity(object):
    """An abstract class within the cim v1.5 type system.

    An abstract class used as the parent of MeasurementCampaigns, Projects, Experiments, and NumericalActivities.
    """
    # Abstract Base Class module.
    # N.B. - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self):
        """Constructor"""
        super(Activity, self).__init__()
        self.funding_sources = []                    # type = str
        self.projects = []                           # type = activity.ProjectType
        self.rationales = []                         # type = str
        self.responsible_parties = []                # type = shared.ResponsibleParty


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
        append(d, 'funding_sources', self.funding_sources, True, True, False)
        append(d, 'projects', self.projects, True, False, True)
        append(d, 'rationales', self.rationales, True, True, False)
        append(d, 'responsible_parties', self.responsible_parties, True, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

