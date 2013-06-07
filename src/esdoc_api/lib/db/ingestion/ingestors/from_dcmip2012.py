"""
.. module:: esdoc_api.lib.db.ingestion.ingestors.from_cmip5_questionnaire
   :platform: Unix, Windows
   :synopsis: DCMIP 2012 atom feed ingestor.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from lxml import etree as et

from esdoc_api.lib.db.ingestion.base_ingestor_from_feed import FeedIngestorBase
from esdoc_api.lib.utils.xml_utils import *
from esdoc_api.models.entities import *
from esdoc_api.lib.pyesdoc.ontologies.constants import *


# Project identifier.
_PROJECT = 'DCMIP-2012'

# Schema identifier.
_SCHEMA = CIM_SCHEMA_1_5



class FromDCMIP2012Ingestor(FeedIngestorBase):
    """Manages ingestion from a dcmip 2012 atom feed.

    :ivar endpoint: Ingestion endpoint being processed.
    
    """
    def __init__(self, endpoint):
        """Constructor.

        :param endpoint: Ingestion endpoint being processed (i.e. DCMIP2012 feed).
        :type endpoint: esdoc_api.models.entities.IngestEndpoint
        
        """
        super(FromDCMIP2012Ingestor, self).__init__(endpoint,
                                                    _PROJECT,
                                                    _SCHEMA,
                                                    url_parser=self.parse_entry_url,
                                                    content_parser=self.parse_entry_content)
    

    def parse_entry_url(self, url):
        """Parses feed entry url's in order to correct errors on feed setup.

        :param url: Feed entry url.
        :type content: str
        :returns: Parsed feed entry url.
        :rtype: str

        """
        if url.startswith('http://hydra.fsl.noaa.gov/content/'):
            url = url.replace('http://hydra.fsl.noaa.gov/content/',
                              'http://hydra.fsl.noaa.gov/cim-atom-feed/feeds/cim/content/')
        return url


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
        :rtype: esdoc_api.models.entities.Document

        """
        # Set etree representation.
        etree = et.fromstring(content)
        nsmap = etree.nsmap
        nsmap["cim"] = nsmap.pop(None)

        # Restrict ingest to model components.
        if cim_tag(etree) == CIM_TAG_MODEL_COMPONENT:
            self.ingest_document(etree, nsmap)


    def on_feed_ingested(self):
        """Callback invoked when a feed has been ingested.

        """
        pass
