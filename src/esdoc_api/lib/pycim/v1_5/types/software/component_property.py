"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.550422.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.data_source import DataSource
from esdoc_api.lib.pycim.v1_5.types.shared.citation import Citation
from esdoc_api.lib.pycim.v1_5.types.software.component_property_intent_type import ComponentPropertyIntentType
from esdoc_api.lib.pycim.v1_5.types.shared.unit_type import UnitType



# Module exports.
__all__ = ['ComponentProperty']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.550422$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class ComponentProperty(DataSource):
    """A concrete class within the cim v1.5 type system.

    ComponentProperties include things that a component simulates (ie: pressure, humidity) and things that prescribe that simulation (ie: gravity, choice of advection scheme). Note that this is a specialisation of shared::DataSource. data::DataObject is also a specialisation of shared::DataSource. This allows software::Connections and/or activity::Conformance to refer to either ComponentProperties or DataObjects.
    """

    def __init__(self):
        """Constructor"""
        super(ComponentProperty, self).__init__()
        self.children = []                           # type = software.ComponentProperty
        self.citations = []                          # type = shared.Citation
        self.description = str()                     # type = str
        self.grid = str()                            # type = str
        self.intent = ''                             # type = software.ComponentPropertyIntentType
        self.is_represented = bool()                 # type = bool
        self.long_name = str()                       # type = str
        self.short_name = str()                      # type = str
        self.standard_names = []                     # type = str
        self.units = ''                              # type = shared.UnitType
        self.values = []                             # type = str


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
        d = dict(super(ComponentProperty, self).as_dict())
        append(d, 'children', self.children, True, False, False)
        append(d, 'citations', self.citations, True, False, False)
        append(d, 'description', self.description, False, True, False)
        append(d, 'grid', self.grid, False, True, False)
        append(d, 'intent', self.intent, False, False, True)
        append(d, 'is_represented', self.is_represented, False, True, False)
        append(d, 'long_name', self.long_name, False, True, False)
        append(d, 'short_name', self.short_name, False, True, False)
        append(d, 'standard_names', self.standard_names, True, True, False)
        append(d, 'units', self.units, False, False, True)
        append(d, 'values', self.values, True, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

