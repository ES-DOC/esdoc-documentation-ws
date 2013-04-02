"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.544096.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.
from esdoc_api.lib.pycim.v1_5.types.shared.responsible_party_contact_info import ResponsiblePartyContactInfo



# Module exports.
__all__ = ['ResponsibleParty']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.544096$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class ResponsibleParty(object):
    """A concrete class within the cim v1.5 type system.

    A person/organsiation responsible for some aspect of a climate science artefact
    """

    def __init__(self):
        """Constructor"""
        super(ResponsibleParty, self).__init__()
        self.abbreviation = str()                    # type = str
        self.contact_info = None                     # type = shared.ResponsiblePartyContactInfo
        self.individual_name = str()                 # type = str
        self.organisation_name = str()               # type = str
        self.role = str()                            # type = str


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
        append(d, 'abbreviation', self.abbreviation, False, True, False)
        append(d, 'contact_info', self.contact_info, False, False, False)
        append(d, 'individual_name', self.individual_name, False, True, False)
        append(d, 'organisation_name', self.organisation_name, False, True, False)
        append(d, 'role', self.role, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

