"""Exposes functions for decoding/encoding cim instances.

"""

# Module imports.
from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import CIM_ENCODINGS
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS
from esdoc_api.lib.pycim.core.decoding.cim_decoder import decode as decode_instance
from esdoc_api.lib.pycim.core.encoding.cim_encoder import encode as encode_representation

# Module exports.
__all__ = ['decode', 'encode']



def decode(representation, schema, encoding):
    """Decodes a CIM instance from passed representation & encoding.

    Keyword arguments:
    representation -- a representation of a CIM instance.
    schema -- cim schema that representation conforms to.
    encoding -- type of representation to decode.

    """
    # Defensive programming.
    if representation is None:
        raise CIMException('CIM instances cannot be decoded from null objects.')
    if schema not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM schema.'.format(schema))
    if encoding not in CIM_ENCODINGS:
        raise CIMException('{0} is an unsupported CIM encoding.'.format(encoding))

    return decode_instance(representation, schema, encoding)



def encode(instance, schema, encoding):
    """Encodes a representation of passed encoding from passed CIM instance.

    Keyword arguments:
    instance -- instance of a CIM type.
    version -- cim version that instance conforms to.
    encoding -- type of representation to encode.

    """
    # Defensive programming.
    if instance is None:
        raise CIMException('Cannot encode null objects.')
    if schema not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM schema.'.format(schema))
    if encoding not in CIM_ENCODINGS:
        raise CIMException('{0} is an unsupported CIM encoding.'.format(encoding))

    return encode_representation(instance, schema, encoding)


