"""Encapsulates xml utility functions.

"""

# Module imports.
import lxml
from lxml import etree as et

from esdoc_api.lib.utils.cim_exception import CIMException

# Module exports.
__all__ = ['as_xml', 
           'deserialize_cim_xml',
           'cim_element_name',
           'cim_element',
           'cim_tag',
           'apply_xpath',
           'CIM15_NS',
           'CIM16_NS',
           'CIM17_NS',
           'CIM18_NS',
           'CIM19_NS',
           'CIM_TAGS',
           'CIM_TAG_ASSIMILATION',
           'CIM_TAG_DATA_OBJECT',
           'CIM_TAG_DATA_PROCESSING',
           'CIM_TAG_DOCUMENT_SET',
           'CIM_TAG_ENSEMBLE',
           'CIM_TAG_GRID_SPEC',
           'CIM_TAG_MODEL_COMPONENT',
           'CIM_TAG_NUMERICAL_EXPERIMENT',
           'CIM_TAG_PLATFORM',
           'CIM_TAG_PROCESSOR_COMPONENT',
           'CIM_TAG_QUALITY',
           'CIM_TAG_SIMULATION_COMPOSITE',
           'CIM_TAG_SIMULATION_RUN',
]

# CIM xml namespaces.
CIM15_NS = 'http://www.purl.org/org/esmetadata/cim/1.5/schemas'
CIM16_NS = 'http://www.purl.org/org/esmetadata/cim/1.6/schemas'
CIM17_NS = 'http://www.purl.org/org/esmetadata/cim/1.7/schemas'
CIM18_NS = 'http://www.purl.org/org/esmetadata/cim/1.8/schemas'
CIM19_NS = 'http://www.purl.org/org/esmetadata/cim/1.9/schemas'

# CIM xml external namespaces.
GMDNS = 'http://www.isotc211.org/2005/gmd'
GCONS = 'http://www.isotc211.org/2005/gco'
XSINS = 'http://www.w3.org/2001/XMLSchema-instance'


# Set of supported cim tags.
CIM_TAG_ASSIMILATION = 'assimilation'
CIM_TAG_DATA_OBJECT = 'dataObject'
CIM_TAG_DATA_PROCESSING = 'dataProcessing'
CIM_TAG_DOCUMENT_SET = 'CIMDocumentSet'
CIM_TAG_ENSEMBLE = 'ensemble'
CIM_TAG_GRID_SPEC = 'gridSpec'
CIM_TAG_MODEL_COMPONENT = 'modelComponent'
CIM_TAG_NUMERICAL_EXPERIMENT = 'numericalExperiment'
CIM_TAG_PLATFORM = 'platform'
CIM_TAG_PROCESSOR_COMPONENT = 'processorComponent'
CIM_TAG_QUALITY = 'cIM_Quality'
CIM_TAG_SIMULATION_COMPOSITE = 'simulationComposite'
CIM_TAG_SIMULATION_RUN = 'simulationRun'


# Collection of supported cim tags.
CIM_TAGS = [
    CIM_TAG_ASSIMILATION,
    CIM_TAG_DATA_OBJECT,
    CIM_TAG_DATA_PROCESSING,
    CIM_TAG_DOCUMENT_SET,
    CIM_TAG_ENSEMBLE,
    CIM_TAG_GRID_SPEC,
    CIM_TAG_MODEL_COMPONENT,
    CIM_TAG_NUMERICAL_EXPERIMENT,
    CIM_TAG_PLATFORM,
    CIM_TAG_PROCESSOR_COMPONENT,
    CIM_TAG_QUALITY,
    CIM_TAG_SIMULATION_COMPOSITE,
    CIM_TAG_SIMULATION_RUN,
]


def _extend_xpath_functions():
    """Adds functions available to xpath expressions.

    Essentially fills holes in lxml xpath 2.0 conformance.
    """
    def make_lower_case(ctxt, s):
        return s.lower()

    def make_upper_case(ctxt, s):
        return s.upper()

    ns = et.FunctionNamespace(None)
    ns['lower-case'] = make_lower_case
    ns['upper-case'] = make_upper_case

_extend_xpath_functions()


def as_xml(root_tag, node_tag, node_list, as_string=False):
    """Factory method to create an etree element and append node list.

    Keyword arguments:
    root_tag -- name of root tag.
    node_list -- collection of node to append.

    """
    # Defensive programming.
    if root_tag is None or \
       isinstance(root_tag, basestring) == False:
        raise TypeError("root_tag must be a string.")
    if node_tag is None or \
       isinstance(node_tag, basestring) == False:
        raise TypeError("node_tag must be a string.")

    # Build xml.
    root = et.Element(root_tag)
    for node in node_list:
        et.SubElement(root, node_tag).text = node

    # Return as requested.
    if as_string:
        return et.tostring(root)
    else:
        return root


def deserialize_cim_xml(xml, return_nsmap=False):
    """Deserializes cim instance to an etree element.
    
    Keyword arguments:
    xml -- an xml representation of a cim instance.
    return_nsmap -- flag indicating whether namespace map will be returned or not.

    """
    # Defensive programming.
    if xml is None:
        raise CIMException("CIM instance as xml is undefined.")
    
    nsmap = None
    
    # ... etree elements.
    if isinstance(xml, et._Element):
        nsmap = xml.nsmap

    # ... etree element trees.
    elif isinstance(xml, et._ElementTree):
        xml = xml.getroot()
        nsmap = xml.nsmap

    else:
        # ... files / URLs.
        try:
            xml = et.parse(xml)
            xml = xml.getroot()
            nsmap = xml.nsmap
        except Exception as e:
            # ... strings.
            if isinstance(xml, basestring):
                try:
                    xml = et.fromstring(xml)
                    nsmap = xml.nsmap
                except Exception:
                    raise CIMException("Invalid cim instance xml string.")
            else:
                raise CIMException("Unsupported cim_instance xml type, must be either a string, file, url or etree.")

    # Guarantees that cim is default namespace.
    if nsmap is not None:
        nsmap['cim'] = nsmap.pop(None)

    # Return either a tuple or single.
    if return_nsmap == True:
        return xml, nsmap
    else:
        return xml


def cim_element_name(tag, ns=CIM15_NS):
    """Returns name of first mathcing element.

    Keyword arguments:
    xml -- etree xml node against which to apply xpath.
    tag -- name of tag being searched for.
    ns -- contextual namespace.

    """
    result = '{'
    result += ns
    result += '}'
    result += tag
    return result


def cim_element(xml_node, tag, ns=CIM15_NS):
    """Returns first matching element.

    Keyword arguments:
    xml -- etree xml node against which to apply xpath.
    tag -- name of tag being searched for.
    ns -- contextual namespace.

    """
    return xml_node.find(cim_element_name(tag, ns))


def cim_tag(xml, cim_ns=CIM15_NS):
    """Returns cim tag from passed node.

    Keyword arguments:
    xml -- etree xml node being processed.
    cim_ns -- contextual namespace.

    """
    result = xml.tag
    if isinstance(cim_ns, list) == False:
        cim_ns = [cim_ns]
    for ns in cim_ns:
        result = result.replace('{' + ns + '}', '')
    return result


def apply_xpath(xml_source, xpath):
    """Applies an xpath expression to target xml & returns etree element.

    Keyword arguments:
    target_xml -- target xml against which to apply xpath.
    xpath -- xpath to apply.

    """
    import types

    # Defensive programming.
    if xml_source is None or xpath is None:
        return None

    # Process string, function, etree element.
    if isinstance(xml_source, basestring):
        return et.fromstring(xml_source).xpath(xpath)
    elif isinstance(xml_source, types.FunctionType):
        return apply_xpath(xml_source(), xpath)
    elif isinstance(xml_source, et._Element):
        return xml_source.xpath(xpath)
    else:
        raise TypeError("xml_source must be either a string, a function, or an etree element.")





