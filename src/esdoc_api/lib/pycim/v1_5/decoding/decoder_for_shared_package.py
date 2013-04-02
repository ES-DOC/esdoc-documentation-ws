"""A set of cim 1.5 decodings.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.447628.
"""

# Module imports.
from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml_utils import *
from esdoc_api.lib.pycim.v1_5.types.shared import *


# Module exports.
__all__ = [
    "decode_calendar", 
    "decode_change", 
    "decode_change_property", 
    "decode_cim_document_relationship", 
    "decode_cim_document_relationship_target", 
    "decode_cim_genealogy", 
    "decode_cim_info", 
    "decode_cim_reference", 
    "decode_cim_relationship", 
    "decode_cim_type_info", 
    "decode_citation", 
    "decode_closed_date_range", 
    "decode_compiler", 
    "decode_daily_360", 
    "decode_data_source", 
    "decode_date_range", 
    "decode_license", 
    "decode_machine", 
    "decode_machine_compiler_unit", 
    "decode_open_date_range", 
    "decode_perpetual_period", 
    "decode_platform", 
    "decode_property", 
    "decode_real_calendar", 
    "decode_responsible_party", 
    "decode_responsible_party_contact_info", 
    "decode_standard", 
    "decode_standard_name"
]


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="2013-01-30 15:45:18.447628"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"


def decode_calendar(xml, nsmap):
    """Decodes a calendar instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('length', False, 'int', 'child::cim:length'),
        ('range', False, decode_closed_date_range, 'child::cim:range/cim:closedDateRange'),
        ('range', False, decode_open_date_range, 'child::cim:range/cim:openDateRange'),
    ]

    return set_attributes(Calendar(), xml, nsmap, decodings)


def decode_change(xml, nsmap):
    """Decodes a change instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('author', False, decode_responsible_party, 'child::cim:changeAuthor'),
        ('date', False, 'datetime', 'child::cim:changeDate'),
        ('description', False, 'str', 'child::cim:description'),
        ('details', True, decode_change_property, 'child::cim:detail'),
        ('name', False, 'str', 'child::cim:name'),
        ('type', False, 'str', 'self::cim:change/@type'),
    ]

    return set_attributes(Change(), xml, nsmap, decodings)


def decode_change_property(xml, nsmap):
    """Decodes a change property instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('id', False, 'str', 'child::cim:id'),
        ('name', False, 'str', 'child::cim:name'),
        ('value', False, 'str', 'child::cim:value'),
    ]

    return set_attributes(ChangeProperty(), xml, nsmap, decodings)


def decode_cim_document_relationship(xml, nsmap):
    """Decodes a cim document relationship instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('direction', False, 'str', 'self::cim:documentRelationship/@direction'),
        ('target', False, decode_cim_document_relationship_target, 'child::cim:target'),
        ('type', False, 'str', 'self::cim:documentRelationship/@type'),
    ]

    return set_attributes(CimDocumentRelationship(), xml, nsmap, decodings)


def decode_cim_document_relationship_target(xml, nsmap):
    """Decodes a cim document relationship target instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('reference', False, decode_cim_reference, 'child::cim:reference'),
    ]

    return set_attributes(CimDocumentRelationshipTarget(), xml, nsmap, decodings)


def decode_cim_genealogy(xml, nsmap):
    """Decodes a cim genealogy instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('relationships', True, decode_cim_document_relationship, 'child::cim:relationship/cim:documentRelationship'),
    ]

    return set_attributes(CimGenealogy(), xml, nsmap, decodings)


def decode_cim_info(xml, nsmap):
    """Decodes a cim info instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('author', False, decode_responsible_party, 'child::cim:documentAuthor'),
        ('create_date', False, 'datetime', 'child::cim:documentCreationDate'),
        ('external_ids', True, decode_standard_name, 'child::cim:externalID'),
        ('genealogy', False, decode_cim_genealogy, 'child::cim:documentGenealogy'),
        ('id', False, 'uuid', 'child::cim:documentID'),
        ('version', False, 'str', 'child::cim:documentVersion'),
    ]

    return set_attributes(CimInfo(), xml, nsmap, decodings)


def decode_cim_reference(xml, nsmap):
    """Decodes a cim reference instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('changes', True, decode_change, 'child::cim:change'),
        ('description', False, 'str', 'child::cim:description'),
        ('external_id', False, 'str', 'child::cim:externalID'),
        ('id', False, 'uuid', 'child::cim:id'),
        ('name', False, 'str', 'child::cim:name'),
        ('type', False, 'str', 'child::cim:type'),
        ('version', False, 'str', 'child::cim:version'),
    ]

    return set_attributes(CimReference(), xml, nsmap, decodings)


def decode_cim_relationship(xml, nsmap):
    """Decodes a cim relationship instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
    ]

    return set_attributes(CimRelationship(), xml, nsmap, decodings)


def decode_cim_type_info(xml, nsmap):
    """Decodes a cim type info instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
    ]

    return set_attributes(CimTypeInfo(), xml, nsmap, decodings)


def decode_citation(xml, nsmap):
    """Decodes a citation instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('alternative_title', False, 'str', 'child::gmd:alternateTitle/gco:CharacterString'),
        ('collective_title', False, 'str', 'gmd:collectiveTitle/gco:CharacterString'),
        ('date', False, 'datetime', 'child::gmd:date/gmd:CI_Date/gmd:date/gco:Date'),
        ('date_type', False, 'str', 'child::gmd:date/gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode/@codeListValue'),
        ('location', False, 'str', 'child::gmd:otherCitationDetails/gco:CharacterString'),
        ('title', False, 'str', 'child::gmd:title/gco:CharacterString'),
        ('type', False, 'str', 'child::gmd:presentationForm/gmd:CI_PresentationFormCode/@codeListValue'),
    ]

    return set_attributes(Citation(), xml, nsmap, decodings)


def decode_closed_date_range(xml, nsmap):
    """Decodes a closed date range instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('duration', False, 'str', 'child::cim:duration'),
        ('end', False, 'datetime', 'child::cim:endDate'),
        ('start', False, 'datetime', 'child::cim:startDate'),
    ]

    return set_attributes(ClosedDateRange(), xml, nsmap, decodings)


def decode_compiler(xml, nsmap):
    """Decodes a compiler instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('environment_variables', False, 'str', 'child::cim:compilerEnvironmentVariables'),
        ('language', False, 'str', 'child::cim:compilerLanguage'),
        ('name', False, 'str', 'child::cim:compilerName'),
        ('options', False, 'str', 'child::cim:compilerOptions'),
        ('type', False, 'str', 'child::cim:compilerType'),
        ('version', False, 'str', 'child::cim:compilerVersion'),
    ]

    return set_attributes(Compiler(), xml, nsmap, decodings)


def decode_daily_360(xml, nsmap):
    """Decodes a daily 360 instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('length', False, 'int', 'child::cim:length'),
        ('range', False, decode_closed_date_range, 'child::cim:range/cim:closedDateRange'),
        ('range', False, decode_open_date_range, 'child::cim:range/cim:openDateRange'),
    ]

    return set_attributes(Daily360(), xml, nsmap, decodings)


def decode_data_source(xml, nsmap):
    """Decodes a data source instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
    ]

    return set_attributes(DataSource(), xml, nsmap, decodings)


def decode_date_range(xml, nsmap):
    """Decodes a date range instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('duration', False, 'str', 'child::cim:duration'),
    ]

    return set_attributes(DateRange(), xml, nsmap, decodings)


def decode_license(xml, nsmap):
    """Decodes a license instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
    ]

    return set_attributes(License(), xml, nsmap, decodings)


def decode_machine(xml, nsmap):
    """Decodes a machine instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('cores_per_processor', False, 'int', 'child::cim:machineCoresPerProcessor'),
        ('description', False, 'str', 'child::cim:machineDescription'),
        ('interconnect', False, 'str', 'child::cim:machineInterconnect/@value'),
        ('libraries', True, 'str', 'child::cim:machineLibrary'),
        ('location', False, 'str', 'child::cim:machineLocation'),
        ('maximum_processors', False, 'int', 'child::cim:machineMaximumProcessors'),
        ('name', False, 'str', 'child::cim:machineName'),
        ('operating_system', False, 'str', 'child::cim:machineOperatingSystem/@value'),
        ('processor_type', False, 'str', 'child::cim:machineProcessorType/@value'),
        ('system', False, 'str', 'child::cim:machineSystem'),
        ('type', False, 'str', '@machineType'),
        ('vendor', False, 'str', 'child::cim:machineVendor/@value'),
    ]

    return set_attributes(Machine(), xml, nsmap, decodings)


def decode_machine_compiler_unit(xml, nsmap):
    """Decodes a machine compiler unit instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('compilers', True, decode_compiler, 'child::cim:compiler'),
        ('machine', False, decode_machine, 'child::cim:machine'),
    ]

    return set_attributes(MachineCompilerUnit(), xml, nsmap, decodings)


def decode_open_date_range(xml, nsmap):
    """Decodes a open date range instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('duration', False, 'str', 'child::cim:duration'),
        ('end', False, 'datetime', 'child::cim:endDate'),
        ('start', False, 'datetime', 'child::cim:startDate'),
    ]

    return set_attributes(OpenDateRange(), xml, nsmap, decodings)


def decode_perpetual_period(xml, nsmap):
    """Decodes a perpetual period instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('length', False, 'int', 'child::cim:length'),
        ('range', False, decode_closed_date_range, 'child::cim:range/cim:closedDateRange'),
        ('range', False, decode_open_date_range, 'child::cim:range/cim:openDateRange'),
    ]

    return set_attributes(PerpetualPeriod(), xml, nsmap, decodings)


def decode_platform(xml, nsmap):
    """Decodes a platform instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('cim_info', False, decode_cim_info, 'self::cim:platform'),
        ('contacts', True, decode_responsible_party, 'child::cim:contact'),
        ('description', False, 'str', 'child::cim:description'),
        ('long_name', False, 'str', 'child::cim:longName'),
        ('short_name', False, 'str', 'child::cim:shortName'),
        ('units', True, decode_machine_compiler_unit, 'child::cim:unit'),
    ]

    return set_attributes(Platform(), xml, nsmap, decodings)


def decode_property(xml, nsmap):
    """Decodes a property instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('name', False, 'str', 'child::cim:name'),
        ('value', False, 'str', 'child::cim:value'),
    ]

    return set_attributes(Property(), xml, nsmap, decodings)


def decode_real_calendar(xml, nsmap):
    """Decodes a real calendar instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('length', False, 'int', 'child::cim:length'),
        ('range', False, decode_closed_date_range, 'child::cim:range/cim:closedDateRange'),
        ('range', False, decode_open_date_range, 'child::cim:range/cim:openDateRange'),
    ]

    return set_attributes(RealCalendar(), xml, nsmap, decodings)


def decode_responsible_party(xml, nsmap):
    """Decodes a responsible party instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('abbreviation', False, 'str', 'child::cim:abbreviation'),
        ('contact_info', False, decode_responsible_party_contact_info, 'child::gmd:contactInfo/gmd:CI_Contact'),
        ('individual_name', False, 'str', 'child::gmd:individualName/gco:CharacterString'),
        ('organisation_name', False, 'str', 'child::gmd:organisationName/gco:CharacterString'),
        ('role', False, 'str', 'gmd:role/gmd:CI_RoleCode/@codeListValue'),
    ]

    return set_attributes(ResponsibleParty(), xml, nsmap, decodings)


def decode_responsible_party_contact_info(xml, nsmap):
    """Decodes a responsible party contact info instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('address', False, 'str', 'child::gmd:address/gmd:CI_Address/gmd:deliveryPoint/gco:CharacterString'),
        ('email', False, 'str', 'child::gmd:address/gmd:CI_Address/gmd:electronicMailAddress/gco:CharacterString'),
        ('url', False, 'str', 'child::gmd:onlineResource/gmd:CI_OnlineResource/gmd:linkage/gmd:URL'),
    ]

    return set_attributes(ResponsiblePartyContactInfo(), xml, nsmap, decodings)


def decode_standard(xml, nsmap):
    """Decodes a standard instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('name', False, 'str', 'child::cim:name'),
        ('version', False, 'str', 'child::cim:version'),
    ]

    return set_attributes(Standard(), xml, nsmap, decodings)


def decode_standard_name(xml, nsmap):
    """Decodes a standard name instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('is_open', False, 'bool', '@open'),
        ('standards', True, decode_standard, 'child::cim:standard'),
        ('value', False, 'str', '@value'),
    ]

    return set_attributes(StandardName(), xml, nsmap, decodings)


