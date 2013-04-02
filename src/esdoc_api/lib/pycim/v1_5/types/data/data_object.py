"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.508514.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.data_source import DataSource
from esdoc_api.lib.pycim.v1_5.types.shared.cim_info import CimInfo
from esdoc_api.lib.pycim.v1_5.types.shared.citation import Citation
from esdoc_api.lib.pycim.v1_5.types.data.data_content import DataContent
from esdoc_api.lib.pycim.v1_5.types.data.data_property import DataProperty
from esdoc_api.lib.pycim.v1_5.types.data.data_status_type import DataStatusType
from esdoc_api.lib.pycim.v1_5.types.data.data_distribution import DataDistribution
from esdoc_api.lib.pycim.v1_5.types.data.data_extent import DataExtent
from esdoc_api.lib.pycim.v1_5.types.data.data_hierarchy_level import DataHierarchyLevel
from esdoc_api.lib.pycim.v1_5.types.shared.cim_reference import CimReference
from esdoc_api.lib.pycim.v1_5.types.data.data_restriction import DataRestriction
from esdoc_api.lib.pycim.v1_5.types.data.data_storage import DataStorage



# Module exports.
__all__ = ['DataObject']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.508514$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class DataObject(DataSource):
    """A concrete class within the cim v1.5 type system.

    A DataObject describes a unit of data.  DataObjects can be grouped hierarchically.  The attributes hierarchyLevelName and hierarchyLevelValue describe how objects are grouped.
    """

    def __init__(self):
        """Constructor"""
        super(DataObject, self).__init__()
        self.acronym = str()                         # type = str
        self.child_object = []                       # type = data.DataObject
        self.cim_info = None                         # type = shared.CimInfo
        self.citations = []                          # type = shared.Citation
        self.content = []                            # type = data.DataContent
        self.data_property = []                      # type = data.DataProperty
        self.data_status = ''                        # type = data.DataStatusType
        self.description = str()                     # type = str
        self.distribution = None                     # type = data.DataDistribution
        self.extent = None                           # type = data.DataExtent
        self.geometry_model = str()                  # type = str
        self.hierarchy_level = None                  # type = data.DataHierarchyLevel
        self.keyword = str()                         # type = str
        self.parent_object = None                    # type = data.DataObject
        self.parent_object_reference = None          # type = shared.CimReference
        self.restriction = []                        # type = data.DataRestriction
        self.source_simulation = str()               # type = str
        self.storage = []                            # type = data.DataStorage


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
        d = dict(super(DataObject, self).as_dict())
        append(d, 'acronym', self.acronym, False, True, False)
        append(d, 'child_object', self.child_object, True, False, False)
        append(d, 'cim_info', self.cim_info, False, False, False)
        append(d, 'citations', self.citations, True, False, False)
        append(d, 'content', self.content, True, False, False)
        append(d, 'data_property', self.data_property, True, False, False)
        append(d, 'data_status', self.data_status, False, False, True)
        append(d, 'description', self.description, False, True, False)
        append(d, 'distribution', self.distribution, False, False, False)
        append(d, 'extent', self.extent, False, False, False)
        append(d, 'geometry_model', self.geometry_model, False, True, False)
        append(d, 'hierarchy_level', self.hierarchy_level, False, False, False)
        append(d, 'keyword', self.keyword, False, True, False)
        append(d, 'parent_object', self.parent_object, False, False, False)
        append(d, 'parent_object_reference', self.parent_object_reference, False, False, False)
        append(d, 'restriction', self.restriction, True, False, False)
        append(d, 'source_simulation', self.source_simulation, False, True, False)
        append(d, 'storage', self.storage, True, False, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

