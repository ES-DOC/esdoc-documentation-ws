"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.558982.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.software.parallelisation import Parallelisation
from esdoc_api.lib.pycim.v1_5.types.shared.platform import Platform
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference



# Module exports.
__all__ = ['Deployment']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.558982$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Deployment(object):
    """A concrete class within the cim v1.5 type system.

    Gives information about the technical properties of a component: what machine it was run on, which compilers were used, how it was parallised, etc. A deployment basically associates a deploymentDate with a Platform. A deployment only exists if something has been deployed. A platform, in contrast, can exist independently, waiting to be used in deployments.
    """

    def __init__(self):
        """Constructor"""
        super(Deployment, self).__init__()
        self.deployment_date = datetime.datetime.now()# type = datetime.datetime
        self.description = str()                     # type = str
        self.executable_arguments = []               # type = str
        self.executable_name = str()                 # type = str
        self.parallelisation = None                  # type = software.Parallelisation
        self.platform = None                         # type = shared.Platform
        self.platform_reference = None               # type = shared.CimReference


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
        append(d, 'deployment_date', self.deployment_date, False, True, False)
        append(d, 'description', self.description, False, True, False)
        append(d, 'executable_arguments', self.executable_arguments, True, True, False)
        append(d, 'executable_name', self.executable_name, False, True, False)
        append(d, 'parallelisation', self.parallelisation, False, False, False)
        append(d, 'platform', self.platform, False, False, False)
        append(d, 'platform_reference', self.platform_reference, False, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

