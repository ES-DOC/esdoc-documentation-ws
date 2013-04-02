"""A concrete class within the cim v1.5 type system.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.523255.
"""

# Module imports.
import datetime
import simplejson
import types
import uuid

# Intra/Inter-package imports.



# Module exports.
__all__ = ['Evaluation']


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="$2013-01-30 15:45:18.523255$"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"



class Evaluation(object):
    """A concrete class within the cim v1.5 type system.

    
    """

    def __init__(self):
        """Constructor"""
        super(Evaluation, self).__init__()
        self.date = datetime.datetime.now()          # type = datetime.datetime
        self.description = str()                     # type = str
        self.did_pass = bool()                       # type = bool
        self.explanation = str()                     # type = str
        self.specification = str()                   # type = str
        self.specification_hyperlink = str()         # type = str
        self.title = str()                           # type = str
        self.type = str()                            # type = str
        self.type_hyperlink = str()                  # type = str


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
        append(d, 'description', self.description, False, True, False)
        append(d, 'did_pass', self.did_pass, False, True, False)
        append(d, 'explanation', self.explanation, False, True, False)
        append(d, 'specification', self.specification, False, True, False)
        append(d, 'specification_hyperlink', self.specification_hyperlink, False, True, False)
        append(d, 'title', self.title, False, True, False)
        append(d, 'type', self.type, False, True, False)
        append(d, 'type_hyperlink', self.type_hyperlink, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm

