"""CIM json encoding functions.

"""

# Module imports.
import datetime
import simplejson
import uuid

from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS
from esdoc_api.lib.pycim.core.utils.dict_utils import convert_dict_keys
from esdoc_api.lib.pycim.core.utils.string_utils import convert_to_pascal_case


# Module exports.
__all__ = ['encode']


class JSONEncoder(simplejson.JSONEncoder):
    """
    Extends simplejson to handle specific types.
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat().replace('T', ' ')
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        else:
            return simplejson.JSONEncoder.default(self, obj)


def encode(instance, version):
    """Encodes an json representation of passed CIM instance.

    Keyword arguments:
    instance -- instance of a CIM type.
    version -- cim version that instance conforms to.

    """
    # Defensive programming.
    if instance is None:
        raise CIMException('Cannot encode null instances.')
    if version not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM version.'.format(version))

    # Get dictionary representation of instance.
    d = instance.as_dict()

    # Ensure json naming conventions are honoured.
    d = convert_dict_keys(d, convert_to_pascal_case)

    # Convert dictionary representation of instance to json.
    return JSONEncoder().encode(d)
