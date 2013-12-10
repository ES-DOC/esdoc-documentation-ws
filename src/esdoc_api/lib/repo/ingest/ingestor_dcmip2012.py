"""
.. module:: esdoc_api.lib.repo.ingest.ingestors.from_cmip5_questionnaire.py
   :platform: Unix, Windows
   :synopsis: DCMIP 2012 atom feed ingestor.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from lxml import etree as et

from esdoc_api.lib.repo.ingest.base_ingestor_from_feed import FeedIngestorBase
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.models import *
import esdoc_api.lib.utils.cim_v1 as cim_v1


# Project identifier.
_PROJECT = 'DCMIP-2012'

# Ontology.
_ONTOLOGY = 'cim.1'



class Ingestor(FeedIngestorBase):
    """Manages ingestion from a dcmip 2012 atom feed.

    :ivar endpoint: Ingestion endpoint being processed.
    
    """
    def __init__(self, endpoint):
        """Constructor.

        :param endpoint: Ingestion endpoint being processed (i.e. DCMIP2012 feed).
        :type endpoint: esdoc_api.models.IngestEndpoint
        
        """
        super(Ingestor, self).__init__(endpoint,
                                       _PROJECT,
                                       _ONTOLOGY,
                                       content_parser=self.parse_entry_content)
    

    def parse_entry_content(self, content):
        """Parses feed entry content.

        :param content: Feed entry content.
        :type content: str
        :returns: Parsed feed entry content.
        :rtype: str

        """
        return content.replace('(+: (DEFAULT: ), 1)', '1')


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

        # Restrict ingest to model components.
        if get_tag_name(etree) == cim_v1.XML_TAG_MODEL_COMPONENT:
            self.ingest_document(etree, nsmap)


