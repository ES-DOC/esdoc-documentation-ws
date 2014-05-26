"""
.. module:: esdoc_api.db.ingest.ingestors.from_cmip5_questionnaire.py
   :platform: Unix, Windows
   :synopsis: CMIP5 Questionnaire atom feed ingestor.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from lxml import etree as et

from . base_ingestor_from_feed import FeedIngestorBase
from .. models import *
from .. import (
    dao,
    utils
    )
from esdoc_api.lib.utils.xml_utils import *
import esdoc_api.lib.utils.cim_v1 as cim_v1
import esdoc_api.lib.utils.runtime as rt



# Project code.
_PROJECT = 'CMIP5'

# Ontology.
_ONTOLOGY = 'cim.1'

# Supported CIM xml schemas.
_CIM_XML_1_5_SCHEMA = 'http://www.purl.org/org/esmetadata/cim/1.5/schemas'
_CIM_XML_1_5_XSD = 'http://www.purl.org/org/esmetadata/cim/1.5/schemas/cim.xsd'

# XPaths for accessing xml fragments.
_XPATH_DOC_SET = '/cim:CIMDocumentSet/*'
_XPATH_DOC_SET_SIMULATION = 'child::cim:simulationRun'
_XPATH_DOC_SET_SIMULATION_ID = 'child::cim:simulationRun/child::cim:documentID/text()'
_XPATH_DOC_SET_SIMULATION_VERSION = 'child::cim:simulationRun/child::cim:documentVersion/text()'
_XPATH_DOC_VERSION_FOR_NUM_EXP = 'self::cim:numericalExperiment/@documentVersion'

# Drs path split.
_DRS_SPLIT = '_'

# Set of model name overrides (workaround for questionnaire bug).
_MODEL_OVERRIDES = {
    'BCC_CSM1.1' : 'BCC-CSM1.1'
}

# Set of institute name overrides (workaround for questionnaire bug).
_INSTITUTE_OVERRIDES = {
    'CMA-BCC' : 'BCC',
    'CNRM-GAME' : 'CNRM-CERFACS',
    'GFDL' : 'NOAA-GFDL',
    'GISS' : 'NASA-GISS',
    'NASA GISS' : 'NASA-GISS',
    'NASA' : 'NASA-GISS',
    'NIMR/KMA' : 'NIMR-KMA',
    'Steve' : 'CSIRO-QCCCE',
}



class Ingestor(FeedIngestorBase):
    """Manages ingestion from a CMIP5 Questionnaire atom feed.

    :ivar endpoint: Ingestion endpoint being processed.

    """
    def __init__(self, endpoint):
        """Constructor."""
        super(Ingestor, self).__init__(endpoint, _PROJECT, _ONTOLOGY,
                                       content_parser=self.parse_feed_entry)


    def _set_institute(self, document):
        """Assigns institute to document."""
        # Escape when assigning institute is unnecessary.
        if document.Institute_ID is not None or \
           document.Type == cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT:
            return

        # Get institute code.
        code = document.as_obj.meta.institute
        if code in _INSTITUTE_OVERRIDES:
            code = _INSTITUTE_OVERRIDES[code]

        # Map code to institute entry in repo.
        institute = dao.get_by_name(Institute, code)
        if institute is None:
            rt.log("WARNING :: institute code unknown :: {0}".format(code))
        else:
            document.Institute_ID = institute.ID


    def _set_ensemble_members(self, simulation, drs):
        """Assigns set of simulation ensemble members."""
        ensembles = [d.as_obj for d in simulation.children if d.Type == cim_v1.TYPE_KEY_ENSEMBLE]
        for ensemble in ensembles:
            for member in ensemble.members:
                for id in member.ensemble_ids:
                    if id.value.upper() != drs.Key_04:
                        id_drs = drs.clone()
                        id_drs.Key_04 = id.value.upper()
                        id_drs.reset_path()


    def _get_drs_keys(self, doc):
        """Returns a set of simulation drs keys."""
        keys = []

        for key in self._get_drs_path(doc).split(_DRS_SPLIT):
            key = key.split(" ")
            keys.append(key[len(key) - 1])

        return keys


    def _get_drs_path(self, doc):
        """Returns a simulation drs path."""
        for id in doc.meta.external_ids:
            for standard in id.standards:
                if standard.name == 'QN_DRS':
                    return id.value.upper()
        return None


    def _ingest_document_set(self, etree, nsmap):
        """Ingests a cim simulation document set."""
        def set_model_and_experiment(left, right=None):
            if right is None:
                right = left
            left.summary.Model = right.summary.Field_02
            left.summary.Experiment = right.summary.Field_03

        def do_ingest(xml, parent=None):
            return self.ingest_document(xml, nsmap, parent)

        simulation = None

        # Ingest simulation document.
        for elem in etree.xpath(_XPATH_DOC_SET, namespaces=nsmap):
            if get_tag_name(elem) == cim_v1.XML_TAG_SIMULATION_RUN:
                simulation = do_ingest(elem)
                break
        if simulation is None:
            rt.throw("CMIP5Q documentset must contain a simulation.")
        set_model_and_experiment(simulation)

        # Ingest associated documents.
        for elem in etree.xpath(_XPATH_DOC_SET, namespaces=nsmap):
            if get_tag_name(elem) != cim_v1.XML_TAG_SIMULATION_RUN:
                doc = do_ingest(elem, simulation.as_obj)
                utils.create_sub_doc(simulation, doc)
                if get_tag_name(elem) not in [
                        cim_v1.XML_TAG_MODEL_COMPONENT,
                        cim_v1.XML_TAG_NUMERICAL_EXPERIMENT
                    ]:
                    set_model_and_experiment(doc, simulation)

        return simulation


    def _process_document_set(self, etree, nsmap):
        """Processes a simulation document set."""
        # Escape if already ingested.
        uid = etree.xpath(_XPATH_DOC_SET_SIMULATION_ID, namespaces=nsmap)[0]
        version = etree.xpath(_XPATH_DOC_SET_SIMULATION_VERSION, namespaces=nsmap)[0]
        simulation = dao.get_document(self.project.ID, uid, version)
        if simulation is not None:
            return

        # Create.
        simulation = self._ingest_document_set(etree, nsmap)

        # Assign drs.
        drs = utils.create_doc_drs(simulation, self._get_drs_keys(simulation.as_obj))
        if drs is not None:
            self._set_ensemble_members(simulation, drs)

        # Assign institute.
        self._set_institute(simulation)
        for child in simulation.children:
            if child.Type not in [cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT]:
                child.Institute_ID = simulation.Institute_ID
            child.IsChild == True

        # Assign summary.
        if drs is not None:
            simulation.Summaries[0].Field_01 = drs.Key_01
            simulation.Summaries[0].Field_02 = drs.Key_02
            simulation.Summaries[0].Field_03 = drs.Key_03
            simulation.Summaries[0].Field_04 = drs.Key_04
            simulation.Summaries[0].Field_05 = drs.Key_05

        # Print.
        msg = "CREATED DOC SET :: ID={0} UID={1} V={2} DOCS={3}."
        rt.log(msg.format(simulation.ID, uid, version, len(simulation.children) + 1))
        rt.log("****************************************************************")

        return simulation


    def _process_document(self, etree, nsmap):
        """Processes a document."""
        # Ingest.
        document = self.ingest_document(etree, nsmap)

        # Perform post deserialization tasks.
        for task in (self._set_institute, ):
            task(document)

        return document


    def parse_feed_entry(self, content):
        """Parses feed entry content.

        :param content: Feed entry content.
        :type content: str
        :returns: Parsed feed entry content.
        :rtype: str

        """
        # Workaround :: Replace erroneous XML schema declaration.
        return content.replace(_CIM_XML_1_5_XSD, _CIM_XML_1_5_SCHEMA)


    def on_doc_decoded(self, doc, etree, nsmap):
        """On document decoded handler.

        :param doc: Deserialized pyesdoc document representation.
        :type doc: python object

        :param etree: Document XML.
        :type etree: lxml.etree

        :param nsmap: Document XML namespaces.
        :type nsmap: dict

        """
        super(Ingestor, self).on_doc_decoded(doc, etree, nsmap)

        def get_institute(responsible_parties):
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


        # Workaround :: Set numerical experiment document version.
        if doc.type_key == cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT and\
           doc.meta.version is None:
            version = etree.xpath(_XPATH_DOC_VERSION_FOR_NUM_EXP, namespaces=nsmap)
            if version is not None and len(version) > 0:
                doc.meta.version = str(version[0])

        # Workaround :: Suppress root model component properties.
        if doc.type_key == cim_v1.TYPE_KEY_MODEL_COMPONENT:
            doc.properties = []

        # Workaround :: Override invalid model names.
        if doc.type_key == cim_v1.TYPE_KEY_MODEL_COMPONENT:
            if doc.short_name in _MODEL_OVERRIDES:
                doc.short_name = _MODEL_OVERRIDES[doc.short_name]

        # Workaround :: Derive institute code - 1.
        if doc.type_key in [cim_v1.TYPE_KEY_MODEL_COMPONENT, cim_v1.TYPE_KEY_PLATFORM]:
            try:
                doc.meta.institute = get_institute(doc.responsible_parties)
            except AttributeError:
                try:
                    doc.meta.institute = get_institute(doc.contacts)
                except AttributeError:
                    pass

        # Workaround :: Derive institute code - 2.
        if doc.type_key == cim_v1.TYPE_KEY_SIMULATION_RUN:
            drs_keys = self._get_drs_keys(doc)
            if len(drs_keys) > 0:
                doc.meta.institute = drs_keys[0]


    def ingest_feed_entry(self, content):
        """Ingests feed entry currently being processed.

        :param content: Feed entry content.
        :type content: str
        :returns: A deserialized simulation document.
        :rtype: esdoc_api.db.models.Document

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
        elif get_tag_name(etree) == cim_v1.XML_TAG_DOCUMENT_SET:
            return self._process_document_set(etree, nsmap)

        # Process single documents.
        else:
            return self._process_document(etree, nsmap)
