"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.530547.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.responsible_party import ResponsibleParty
from esdoc_api.lib.pycim.v1_5.types.shared.standard_name import StandardName
from esdoc_api.lib.pycim.v1_5.types.shared.cim_genealogy import CimGenealogy
from esdoc_api.lib.pycim.v1_5.types.shared.document_status_type import DocumentStatusType
from esdoc_api.lib.pycim.v1_5.types.shared.cim_type_info import CimTypeInfo



# Module exports.
__all__ = ['CimInfo']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.530547$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class CimInfo(object):
    """A concrete class within the cim v1.5 type system.

    Encapsulates common cim information.
    """

    def __init__(self):
        """Constructor"""
        super(CimInfo, self).__init__()
        self.author = None                           # type = shared.ResponsibleParty
        self.create_date = datetime.datetime.now()   # type = datetime.datetime
        self.external_ids = []                       # type = shared.StandardName
        self.genealogy = None                        # type = shared.CimGenealogy
        self.id = uuid.uuid4()                       # type = uuid.UUID
        self.language = str()                        # type = str
        self.metadata_id = str()                     # type = str
        self.metadata_version = str()                # type = str
        self.project = str()                         # type = str
        self.source = str()                          # type = str
        self.status = ''                             # type = shared.DocumentStatusType
        self.type_info = None                        # type = shared.CimTypeInfo
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
        append(d, 'author', self.author, False, False, False)
        append(d, 'create_date', self.create_date, False, True, False)
        append(d, 'external_ids', self.external_ids, True, False, False)
        append(d, 'genealogy', self.genealogy, False, False, False)
        append(d, 'id', self.id, False, True, False)
        append(d, 'language', self.language, False, True, False)
        append(d, 'metadata_id', self.metadata_id, False, True, False)
        append(d, 'metadata_version', self.metadata_version, False, True, False)
        append(d, 'project', self.project, False, True, False)
        append(d, 'source', self.source, False, True, False)
        append(d, 'status', self.status, False, False, True)
        append(d, 'type_info', self.type_info, False, False, False)
        append(d, 'version', self.version, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

