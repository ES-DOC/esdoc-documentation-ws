"""Exposes functions for decoding cim instances from representations.

"""

# Module imports.
from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import CIM_ENCODINGS
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS
from esdoc_api.lib.pycim.core.decoding.cim_decoder_json import decode as decode_from_json
from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml import decode as decode_from_xml

# Module exports.
__all__ = ['decode']


# Set of decoders by encoding type.
_decoders = {
    'json' : decode_from_json,
    'xml' : decode_from_xml,
}


def decode(representation, schema, encoding):
    """Decodes a CIM instance from passed representation & encoding.

    Keyword arguments:
    representation -- a representation of a CIM instance.
    schema -- cim schema that representation conforms to.
    encoding -- type of representation to decode.

    """
    # Defensive programming.
    if representation is None:
        raise CIMException('Cannot decode null representations.')
    if schema not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM version.'.format(schema))
    if encoding not in CIM_ENCODINGS:
        raise CIMException('{0} is an unsupported CIM encoding.'.format(encoding))

    # Decode instance from representation.
    return _decoders[encoding](representation, schema)


