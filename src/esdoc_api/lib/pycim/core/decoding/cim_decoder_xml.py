"""CIM xml decoding functions.

"""
# Module imports.
from lxml import etree as et

from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml_utils import get_cim_xml
from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml_utils import decode_xml
from esdoc_api.lib.pycim.core.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import CIM_SCHEMAS
from esdoc_api.lib.pycim.v1_5.types.shared.cim_type_info import CimTypeInfo
import esdoc_api.lib.pycim.v1_5.decoding as v1_5_decoders


# Module exports.
_all__ = ['decode']



# Set of decoders grouped by cim version.
_decoders = {
    '1.5' : {
        'cIM_Quality' : v1_5_decoders.decode_cim_quality,
        'dataObject' : v1_5_decoders.decode_data_object,
        'ensemble' : v1_5_decoders.decode_ensemble,
        'gridSpec' : v1_5_decoders.decode_grid_spec,
        'modelComponent' : v1_5_decoders.decode_model_component,
        'numericalExperiment' : v1_5_decoders.decode_numerical_experiment,
        'platform' : v1_5_decoders.decode_platform,
        'simulationRun' : v1_5_decoders.decode_simulation_run,
        'simulationComposite' : v1_5_decoders.decode_simulation_composite,
    }
}

# Set of type information injected into decoded objects.
_type_info = {
    '1.5' : {
        'cIM_Quality' : ('quality', 'Quality'),
        'dataObject' : ('data', 'Data Object'),
        'ensemble' : ('activity', 'Ensemble'),
        'gridSpec' : ('grids', 'Grid'),
        'modelComponent' : ('software', 'Model'),
        'numericalExperiment' : ('activity', 'Experiment'),
        'platform' : ('activity', 'Platform'),
        'simulationRun' : ('activity', 'Simulation'),
        'simulationComposite' : ('activity', 'Simulation'),
    }
}


def decode(representation, schema):
    """Decodes a CIM instance from passed xml representation.

    Keyword arguments:
    representation -- an xml representation of a CIM instance (i.e. either a filepath, a url or an etree element).
    schema -- cim schema that representation conforms to.

    """
    # Defensive programming.
    if representation is None:
        raise CIMException('Cannot decode null representations.')
    if schema not in CIM_SCHEMAS:
        raise CIMException('{0} is an unsupported CIM version.'.format(schema))

    # Deserialize xml & associated namespaces.
    xml, nsmap = get_cim_xml(representation, return_nsmap=True)

    # Validate xml.
    if _can_decode_from_xml(xml) == False:
        raise CIMException('Representation failed CIM XML validation.')

    # Get cim type.
    type = xml.tag.split('}')[1]
    
    # Get decoder by type.
    if type not in _decoders[schema]:
        raise CIMException('No decoder exists for the following CIM type :: {0}.'.format(type))
    decoder = _decoders[schema][type]

    # Decode pycim obj.
    obj = decode_xml(decoder, xml, nsmap, None)

    # Assign type info.
    _set_cim_type_info(obj, schema, type)

    return obj


def _set_cim_type_info(obj, schema, type):
    """Injects cim type information into object.

    Keyword Arguments:
    obj - a CIM instance.
    schema -- cim schema that representation conforms to.
    type - cim type.

    """
    if schema in _type_info and type in _type_info[schema]:
        info = _type_info[schema][type]
        obj.cim_info.type_info = CimTypeInfo()
        obj.cim_info.type_info.package = info[0]
        obj.cim_info.type_info.schema = schema
        obj.cim_info.type_info.type = type
        obj.cim_info.type_info.type_display_name = info[1]
    else:
        print "WARNING :: CIM object type information is underivable", schema, type


def _can_decode_from_xml(xml):
    """Determines a priori whether xml is decodeable.

    Keyword Arguments:
    xml - xml representation of a CIM instance.
    
    """
    # Deserialize xml (if necessary).
    if isinstance(xml, et._Element) == False:
        xml = get_cim_xml(xml)

    # False if representation has not been converted to an lxml.etree.
    if isinstance(xml, et._Element) == False:
        return False

    # False if representation is an invalid cim xml instance.
    # TODO - implement via call to CIM validator component.

    # All tests have passed therefore return true.
    return True

















