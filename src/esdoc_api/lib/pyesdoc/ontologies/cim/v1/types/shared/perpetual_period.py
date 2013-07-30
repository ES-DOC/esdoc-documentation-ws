"""
.. module:: cim.v1.types.shared.perpetual_period.py

   :copyright: @2013 Earth System Documentation (http://esdocumentation.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: A concrete class within the cim v1 type system.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@esdocumentation.org>
.. note:: Code generated using esdoc_mp @ 2013-07-17 14:43:15.203284.

"""

# Module imports.
import datetime
import types
import uuid

from esdoc_api.lib.pyesdoc.ontologies.cim.v1.types.shared.calendar import Calendar


class PerpetualPeriod(Calendar):
    """A concrete class within the cim v1 type system.

    
    """

    def __init__(self):
        """Constructor"""
        super(PerpetualPeriod, self).__init__()

    def as_dict(self):
        """Returns a deep dictionary representation.

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
        d = dict(super(PerpetualPeriod, self).as_dict())
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm
