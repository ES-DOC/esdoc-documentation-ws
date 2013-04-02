"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.535487.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.compiler_type import CompilerType



# Module exports.
__all__ = ['Compiler']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.535487$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Compiler(object):
    """A concrete class within the cim v1.5 type system.

    A description of a compiler used on a particular platform.
    """

    def __init__(self):
        """Constructor"""
        super(Compiler, self).__init__()
        self.environment_variables = str()           # type = str
        self.language = str()                        # type = str
        self.name = str()                            # type = str
        self.options = str()                         # type = str
        self.type = ''                               # type = shared.CompilerType
        self.version = str()                         # type = str


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
        append(d, 'environment_variables', self.environment_variables, False, True, False)
        append(d, 'language', self.language, False, True, False)
        append(d, 'name', self.name, False, True, False)
        append(d, 'options', self.options, False, True, False)
        append(d, 'type', self.type, False, False, True)
        append(d, 'version', self.version, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

