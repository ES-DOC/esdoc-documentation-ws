"""
.. module:: esdoc_api.lib.repo.ingest.ingestors.from_cmip5_questionnaire.py
   :platform: Unix, Windows
   :synopsis: CMIP5 quality control atom feed ingestor.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from lxml import etree as et

import esdoc_api.lib.repo.dao as dao

from esdoc_api.lib.repo.ingest.base_ingestor_from_feed import FeedIngestorBase
from esdoc_api.models import *


# Project identifier.
_PROJECT = 'CMIP5'

# Ontology schema name.
_ONTOLOGY_NAME = 'cim'

# Ontology schema version.
_ONTOLOGY_VERSION = '1'


            
class Ingestor(FeedIngestorBase):
    """Manages ingestion from a CMIP5 QC atom feed.

    :ivar endpoint: Ingestion endpoint being processed.

    """
    def __init__(self, endpoint):
        """Constructor.

        :param endpoint: Ingestion endpoint being processed (i.e. CMIP5 quality control feed).
        :type endpoint: esdoc_api.models.IngestEndpoint

        """
        super(Ingestor, self).__init__(endpoint,
                                       _PROJECT,
                                       _ONTOLOGY_NAME,
                                       _ONTOLOGY_VERSION)

    
    def set_institute(self, document):
        """Assign institute to qc document.

        :param document: A document being ingested.
        :type document: esdoc_api.models.Document

        """
        # Escape if no external id has been defined.
        if len(document.as_obj.doc_info.external_ids) == 0:
            return

        # Derive drs.
        drs = document.as_obj.doc_info.external_ids[0].value
        drs = drs.split('.')[2:]

        # Derive institute.
        if len(drs) > 0:
            institute = dao.get_by_name(Institute, drs[0].upper())
            if institute is not None:
                document.Institute_ID = institute.ID


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

        # Ingest document.
        document = self.ingest_document(etree, nsmap)

        # Perform post deserialization tasks.
        self.set_institute(document)

        return document

