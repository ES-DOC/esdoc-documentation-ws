"""CIM xml encoding functions.

"""

# Module imports.
from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS


# Module exports.
__all__ = ['encode']


def encode(instance, version):
    """Encodes an xml representation of passed CIM instance.

    Keyword arguments:
    instance -- instance of a CIM type.
    version -- cim version that instance conforms to.

    """
    # Defensive programming.
    if instance is None:
        raise CIMException('Cannot encode null instances.')
    if version not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM version.'.format(version))
        
    return instance
