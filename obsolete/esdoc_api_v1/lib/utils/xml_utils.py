# -*- coding: utf-8 -*-

"""Encapsulates xml utility functions.

"""
# CIM xml namespaces.
CIM15_NS = 'http://www.purl.org/org/esmetadata/cim/1.5/schemas'
CIM18_NS = 'http://www.purl.org/org/esmetadata/cim/1.8.1/schemas'

# CIM xml namespace set.
CIM_NS_SET = [
    CIM15_NS,
    CIM18_NS
]


def get_element_name(tag, ns=CIM15_NS):
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


def get_element(xml_node, tag, ns=CIM15_NS):
    """Returns first matching element.

    Keyword arguments:
    xml -- etree xml node against which to apply xpath.
    tag -- name of tag being searched for.
    ns -- contextual namespace.

    """
    return xml_node.find(get_element_name(tag, ns))


def get_tag_name(xml, cim_ns=CIM_NS_SET):
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

