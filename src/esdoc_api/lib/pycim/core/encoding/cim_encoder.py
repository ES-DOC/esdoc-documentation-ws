"""Exposes functions for encoding representations from cim instances.

"""

# Module imports.
from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import CIM_ENCODINGS
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS
from esdoc_api.lib.pycim.core.encoding.cim_encoder_json import encode as encode_to_json
from esdoc_api.lib.pycim.core.encoding.cim_encoder_xml import encode as encode_to_xml

# Module exports.
__all__ = ['encode']


# Set of encoders by encoding type.
_encoders = {
    'json' : encode_to_json,
    'xml' : encode_to_xml,
}


def encode(instance, version, encoding):
    """Encodes a representation of passed encoding from passed CIM instance.

    Keyword arguments:
    instance -- instance of a CIM type.
    version -- cim version that instance conforms to.
    encoding -- type of representation to encode.

    """
    # Defensive programming.
    if instance is None:
        raise CIMException('Cannot encode null instances.')
    if version not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM version.'.format(version))
    if encoding not in CIM_ENCODINGS:
        raise CIMException('{0} is an unsupported CIM encoding.'.format(encoding))

    # Encode instance to representation.
    return _encoders[encoding](instance, version)

