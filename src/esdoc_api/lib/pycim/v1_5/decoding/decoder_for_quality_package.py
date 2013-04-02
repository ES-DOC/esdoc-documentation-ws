"""A set of cim 1.5 decodings.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.446785.
"""

# Module imports.
from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml_utils import *
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_shared_package import *
from esdoc_api.lib.pycim.v1_5.types.quality import *


# Module exports.
__all__ = [
    "decode_cim_quality", 
    "decode_evaluation", 
    "decode_measure", 
    "decode_report"
]


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="2013-01-30 15:45:18.446785"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"


def decode_cim_quality(xml, nsmap):
    """Decodes a cim quality instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('cim_info', False, decode_cim_info, 'self::cim:cIM_Quality'),
        ('reports', True, decode_report, 'child::cim:report'),
    ]

    return set_attributes(CimQuality(), xml, nsmap, decodings)


def decode_evaluation(xml, nsmap):
    """Decodes a evaluation instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('date', False, 'datetime', 'child::gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:date/gmd:CI_Date/gmd:date/gco:Date'),
        ('description', False, 'str', 'gmd:evaluationMethodDescription/gco:CharacterString'),
        ('did_pass', False, 'bool', 'child::gmd:result/gmd:DQ_ConformanceResult/gmd:pass/gco:Boolean'),
        ('explanation', False, 'str', 'child::gmd:result/gmd:DQ_ConformanceResult/gmd:explanation/gco:CharacterString'),
        ('specification', False, 'str', 'child::gmd:result/@xlink:title'),
        ('specification_hyperlink', False, 'str', 'child::gmd:result/@xlink:href'),
        ('title', False, 'str', 'child::gmd:result/gmd:DQ_ConformanceResult/gmd:specification/gmd:CI_Citation/gmd:title'),
        ('type', False, 'str', 'child::gmd:result/gmd:DQ_ConformanceResult/gmd:specification/@xlink:title'),
        ('type_hyperlink', False, 'str', 'child::gmd:result/gmd:DQ_ConformanceResult/gmd:specification/@xlink:href'),
    ]

    return set_attributes(Evaluation(), xml, nsmap, decodings)


def decode_measure(xml, nsmap):
    """Decodes a measure instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:measureDescription'),
        ('description', False, 'str', 'parent::cim:report/child::gmd:measureDescription/gco:CharacterString'),
        ('identification', False, 'str', 'child::cim:measureIdentification/gmd:code/gco:CharacterString'),
        ('name', False, 'str', 'child::cim:nameOfMeasure'),
        ('name', False, 'str', 'parent::cim:report/child::gmd:nameOfMeasure/gco:CharacterString'),
    ]

    return set_attributes(Measure(), xml, nsmap, decodings)


def decode_report(xml, nsmap):
    """Decodes a report instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('date', False, 'datetime', 'child::gmd:dateTime/gco:DateTime'),
        ('evaluation', False, decode_evaluation, 'self::cim:report'),
        ('evaluator', False, decode_responsible_party, 'child::cim:evaluator'),
        ('measure', False, decode_measure, 'self::cim:report/cim:measure'),
    ]

    return set_attributes(Report(), xml, nsmap, decodings)


