"""
.. module:: esdoc_api.lib.repo.ingest.ingestors.from_cmip5_questionnaire.py
   :platform: Unix, Windows
   :synopsis: CMIP5 Questionnaire atom feed ingestor.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_1_TYPE_PLATFORM
from lxml import etree as et

from esdoc_api.lib.repo.index.cim_v1.model_component.mapper import map as map_facets_for_model_component
from esdoc_api.lib.repo.index.cim_v1.numerical_experiment.mapper import map as map_facets_for_numerical_experiment
from esdoc_api.lib.repo.ingest.base_ingestor_from_feed import FeedIngestorBase
from esdoc_api.lib.pyesdoc.utils.ontologies import *
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.models import *
from esdoc_api.lib.pyesdoc import (
    CIM_1_TYPE_ENSEMBLE,
    CIM_1_TYPE_MODEL_COMPONENT,
    CIM_1_TYPE_NUMERICAL_EXPERIMENT,
    CIM_1_TYPE_PLATFORM,
    CIM_1_TYPE_SIMULATION_RUN
    )
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt
import esdoc_api.lib.api.comparator_setup as comparator


# Project code.
_PROJECT = 'CMIP5'

# Ontology schema name.
_ONTOLOGY_NAME = 'cim'

# Ontology schema version.
_ONTOLOGY_VERSION = '1'

# Supported CIM xml schemas.
_CIM_XML_1_5_SCHEMA = 'http://www.purl.org/org/esmetadata/cim/1.5/schemas'
_CIM_XML_1_5_XSD = 'http://www.purl.org/org/esmetadata/cim/1.5/schemas/cim.xsd'


# XPaths for accessing document set xml fragments.
_XPATH_DOC_SET = '/cim:CIMDocumentSet/*'
_XPATH_DOC_SET_SIMULATION = 'child::cim:simulationRun'
_XPATH_DOC_SET_SIMULATION_ID = 'child::cim:simulationRun/child::cim:documentID/text()'
_XPATH_DOC_SET_SIMULATION_VERSION = 'child::cim:simulationRun/child::cim:documentVersion/text()'
_XPATH_DOC_VERSION_FOR_NUM_EXP = 'self::cim:numericalExperiment/@documentVersion'

# Drs path split.
_DRS_SPLIT = '_'

# Set of document facet mappers keyed by document type.
_facet_mappers = {
    CIM_1_TYPE_MODEL_COMPONENT : map_facets_for_model_component,
    CIM_1_TYPE_NUMERICAL_EXPERIMENT : map_facets_for_numerical_experiment
}

# Set of model name overrides (workaround for questionnaire bug).
_MODEL_OVERRIDES = {
    'BCC_CSM1.1' : 'BCC-CSM1.1'
}

# Set of comparators associated with CMIP5.
_COMPARATOR_TYPES = [ 'c1' ]



class Ingestor(FeedIngestorBase):
    """Manages ingestion from a CMIP5 Questionnaire atom feed.

    :ivar endpoint: Ingestion endpoint being processed.

    """
    def __init__(self, endpoint):
        """Constructor.

        :param endpoint: Ingestion endpoint being processed (i.e. CMIP5 Metafor questionnaire feed).
        :type endpoint: esdoc_api.models.IngestEndpoint

        """
        super(Ingestor, self).__init__(endpoint,
                                       _PROJECT,
                                       _ONTOLOGY_NAME,
                                       _ONTOLOGY_VERSION,
                                       content_parser=self.parse_feed_entry)


    def parse_feed_entry(self, content):
        """Parses feed entry content.

        :param content: Feed entry content.
        :type content: str
        :returns: Parsed feed entry content.
        :rtype: str

        """
        # Workaround :: Replace erroneous XML schema declaration.
        return content.replace(_CIM_XML_1_5_XSD, _CIM_XML_1_5_SCHEMA)


    def parse_document(self, as_obj, etree, nsmap):
        """Parser over deserialized pyesdoc document.

        :param as_obj: Deserialized pyesdoc document representation.
        :type as_obj: python object

        :param etree: Document XML.
        :type etree: lxml.etree

        :param nsmap: Document XML namespaces.
        :type nsmap: dict

        """
        # Workaround :: Set numerical experiment document version.
        if as_obj.cim_info.type_info.type == CIM_1_TYPE_NUMERICAL_EXPERIMENT and \
           as_obj.cim_info.version is None:
            version = etree.xpath(_XPATH_DOC_VERSION_FOR_NUM_EXP, namespaces=nsmap)
            if version is not None and len(version) > 0:
                as_obj.cim_info.version = str(version[0])

        # Workaround :: Suppress root model component properties.
        if as_obj.cim_info.type_info.type == CIM_1_TYPE_MODEL_COMPONENT:
            as_obj.properties = []
            as_obj.property_tree = []

        # Workaround :: Override invalid model names.
        if as_obj.cim_info.type_info.type == CIM_1_TYPE_MODEL_COMPONENT and \
           as_obj.short_name in _MODEL_OVERRIDES:
            as_obj.short_name = _MODEL_OVERRIDES[as_obj.short_name]
            

    def set_institute(self, document, document_by_drs=None):
        """Assigns institute to document.

        :param document: A document being ingested.
        :param document_by_drs: DRS keys associated with a document.
        :type document: esdoc_api.models.Document        
        :type document_by_drs: esdoc_api.models.DocumentDRS

        """
        # Escape when assigning institute is unnecessary.
        if document.Institute_ID is not None or \
           document.Type == CIM_1_TYPE_NUMERICAL_EXPERIMENT.upper():
            return

        def get_code(responsible_parties):
            code = None
            for rp in responsible_parties:
                if rp.role == 'centre':
                    code = rp.abbreviation
                    break;
            if code is None:
                for rp in responsible_parties:
                    if rp.role == 'contact' and rp.abbreviation is not None:
                        code = rp.abbreviation
                        break;
            return code

        def get_id(name):
            i = dao.get_by_name(Institute, name)
            return i.ID if i is not None else None


        code = None

        # Set institute code from drs path.
        if document_by_drs is not None:
            if document_by_drs.Key_01 is not None :
                code = document_by_drs.Key_01

        # Set institute code from responsibile parties for models and platforms.
        elif document.as_obj is not None and \
             document.Type in [CIM_1_TYPE_MODEL_COMPONENT.upper(), CIM_1_TYPE_PLATFORM.upper()]:
            try:
                code = get_code(document.as_obj.responsible_parties)
            except AttributeError:
                try:
                    code = get_code(document.as_obj.contacts)
                except AttributeError:
                    pass

        # Either assign institute or output warning.
        if code is not None:
            document.Institute_ID = get_id(code)
        else:
            rt.log("WARNING :: institute code unknown :: {0}".format(code))


    def set_ensemble_members(self, simulation, drs):
        """Assigns set of simulation ensemble members.

        :param simulation: A simulation document being ingested.
        :param drs: DRS keys associated with a simulation document.
        :type simulation: esdoc_api.models.Document
        :type drs: esdoc_api.models.DocumentDRS

        """
        for ensemble in [d.as_obj for d in simulation.children
                         if d.Type == CIM_1_TYPE_ENSEMBLE.upper()]:
            for member in ensemble.members:
                for id in member.ensemble_ids:
                    if id.value.upper() != drs.Key_04:
                        id_drs = drs.clone()
                        id_drs.Key_04 = id.value.upper()
                        id_drs.reset_path()


    def set_facets(self, document):
        """Assigns facets derived from an ingested document.

        :param document: A document being ingested.
        :type document: esdoc_api.models.Document

        """
        if not document.IsIndexed:
            type = document.as_obj.cim_info.type_info.type
            if type in _facet_mappers:
                _facet_mappers[type](document.as_obj)
            document.IsIndexed = True


    def get_drs_keys(self, simulation):
        """Returns a set of simulation drs keys.

        :param simulation: A simulation document being ingested.
        :type simulation: esdoc_api.models.Document
        :returns: A set of simulation DRS keys as encoded in XML document.
        :rtype: str

        """
        keys = []
        for key in self.get_drs_path(simulation).split(_DRS_SPLIT):
            key = key.split(" ")
            keys.append(key[len(key) - 1])
        return keys
    

    def get_drs_path(self, simulation):
        """Returns a simulation drs path.

        :param simulation: A simulation document being ingested.
        :type simulation: esdoc_api.models.Document
        :returns: A simulation DRS path as encoded in XML document.
        :rtype: str

        """
        for id in simulation.as_obj.cim_info.external_ids:
            for standard in id.standards:
                if standard.name == 'QN_DRS':
                    return id.value.upper()
        return None


    def ingest_simulation_document_set(self, etree, nsmap):
        """Ingests a cim simulation document set.

        :param etree: Document XML.
        :param nsmap: Document XML namespaces.

        :type etree: lxml.etree
        :type nsmap: dict

        :returns: A deserialized simulation document.
        :rtype: esdoc_api.models.Document

        """
        def do_ingest(xml):
            return self.ingest_document(xml, nsmap, self.parse_document)

        # Ingest simulation document.
        simulation = None        
        for elem in etree.xpath(_XPATH_DOC_SET, namespaces=nsmap):
            if get_tag_name(elem) == CIM_1_TYPE_SIMULATION_RUN:
                simulation = do_ingest(elem)
                break
        if simulation is None:
            rt.throw("CMIP5Q documentset must contain a simulation.")

        # Ingest associated documents.
        for elem in etree.xpath(_XPATH_DOC_SET, namespaces=nsmap):
            if get_tag_name(elem) != CIM_1_TYPE_SIMULATION_RUN:                
                utils.create_sub_document(simulation, do_ingest(elem))                

        return simulation


    def process_simulation_document_set(self, etree, nsmap):
        """Processes a simulation document set.

        :param etree: Document XML.
        :param nsmap: Document XML namespaces.
        :type etree: lxml.etree
        :type nsmap: dict
        :returns: A processsed document set.
        :rtype: esdoc_api.models.Document

        """
        # Escape if already ingested.
        uid = etree.xpath(_XPATH_DOC_SET_SIMULATION_ID, namespaces=nsmap)[0]
        version = etree.xpath(_XPATH_DOC_SET_SIMULATION_VERSION, namespaces=nsmap)[0]
        simulation = dao.get_document(self.project.ID, uid, version)
        if simulation is not None:
            return

        # Create.
        simulation = self.ingest_simulation_document_set(etree, nsmap)

        # Assign drs.
        drs = utils.create_document_drs(simulation, self.get_drs_keys(simulation))
        if drs is not None:
            self.set_ensemble_members(simulation, drs)

        # Assign institute.
        self.set_institute(simulation, drs)
        for child in simulation.children:
            if child.Type not in [CIM_1_TYPE_NUMERICAL_EXPERIMENT.upper()]:
                child.Institute_ID = simulation.Institute_ID
            child.IsChild == True

        # Assign summary.
        if drs is not None:
            simulation.Summaries[0].Field_03 = drs.Key_01
            simulation.Summaries[0].Field_04 = drs.Key_02
            simulation.Summaries[0].Field_05 = drs.Key_03
            simulation.Summaries[0].Field_06 = drs.Key_04
            simulation.Summaries[0].Field_07 = drs.Key_05

        # Print.
        msg = "CREATED DOC SET :: ID={0} UID={1} V={2} DOCS={3}."
        rt.log(msg.format(simulation.ID, uid, version, len(simulation.children) + 1))
        rt.log("****************************************************************")

        return simulation


    def process_document(self, etree, nsmap):
        """Processes a document.

        :param etree: Document XML.
        :param nsmap: Document XML namespaces.
        :type etree: lxml.etree
        :type nsmap: dict
        :returns: A processsed document.
        :rtype: esdoc_api.models.Document

        """
        # Ingest.
        document = self.ingest_document(etree, nsmap, self.parse_document)

        # Perform post deserialization tasks.
        for task in [self.set_institute, self.set_facets]:
            task(document)

        return document


    def ingest_feed_entry(self, content):
        """Ingests feed entry currently being processed.

        :param content: Feed entry content.
        :type content: str
        :returns: A deserialized simulation document.
        :rtype: esdoc_api.models.Document

        """
        # Set etree representation.
        etree = et.fromstring(content)
        nsmap = etree.nsmap
        nsmap["cim"] = nsmap.pop(None)

        # Exclude old documents.
        if nsmap["cim"].find('1.4') != -1:
            rt.log("WARNING :: obsolete document")
            return None
        
        # Process document sets.
        elif get_tag_name(etree) == CIM_1_TYPE_DOCUMENT_SET:
            return self.process_simulation_document_set(etree, nsmap)

        # Process single documents.
        else:
            return self.process_document(etree, nsmap)


    def on_feed_ingested(self):
        """Callback invoked when a feed has been ingested.

        """
        # Write comparator json files.
        for type in _COMPARATOR_TYPES:
            comparator.write_comparator_json(_PROJECT, type)


