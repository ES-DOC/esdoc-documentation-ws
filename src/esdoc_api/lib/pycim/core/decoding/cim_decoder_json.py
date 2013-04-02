"""CIM json decoding functions.

"""

# Module imports.
import simplejson

from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS

# Module exports.
_all__ = ['decode']


def decode(representation, schema):
    """Decodes a CIM instance from passed json representation.

    Keyword arguments:
    representation -- a json representation of a CIM instance.
    schema -- cim schema that representation conforms to.

    """
    # Defensive programming.
    if representation is None:
        raise CIMException('Cannot decode null representations.')
    if schema not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM version.'.format(schema))

    as_dict = simplejson.loads(representation)
    
    # TODO convert dictionary to object.
    return as_dict
