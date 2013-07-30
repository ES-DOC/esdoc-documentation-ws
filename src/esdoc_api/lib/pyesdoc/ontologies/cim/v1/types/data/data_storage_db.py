"""
.. module:: cim.v1.types.data.data_storage_db.py

   :copyright: @2013 Earth System Documentation (http://esdocumentation.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: A concrete class within the cim v1 type system.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@esdocumentation.org>
.. note:: Code generated using esdoc_mp @ 2013-07-17 14:43:15.185866.

"""

# Module imports.
import datetime
import types
import uuid

from esdoc_api.lib.pyesdoc.ontologies.cim.v1.types.data.data_storage import DataStorage


class DataStorageDb(DataStorage):
    """A concrete class within the cim v1 type system.

    Contains attributes to describe a DataObject stored as a database file.
    """

    def __init__(self):
        """Constructor"""
        super(DataStorageDb, self).__init__()
        self.access_string = str()                   # type = str
        self.name = str()                            # type = str
        self.owner = str()                           # type = str
        self.table = str()                           # type = str


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
        d = dict(super(DataStorageDb, self).as_dict())
        append(d, 'access_string', self.access_string, False, True, False)
        append(d, 'name', self.name, False, True, False)
        append(d, 'owner', self.owner, False, True, False)
        append(d, 'table', self.table, False, True, False)
        return d


# Circular reference imports.
# N.B. - see http://effbot.org/zone/import-confusion.htm
