"""
.. module:: esdoc_api.lib.repo.ingest.base_ingestor_from_feed.py
   :platform: Unix, Windows
   :synopsis: Base class for all feed ingestors.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from abc import abstractmethod
import urllib2

import feedparser
from lxml import etree as et

from esdoc_api.lib.repo.ingest.base_ingestor import IngestorBase
from esdoc_api.models import *
import esdoc_api.lib.pyesdoc as pyesdoc
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt



class FeedReader(object):
    """Atom/RSS feed reader - wraps feedparser.

    :ivar feed_url: Feed URL.
    :ivar auto_open: Feed URL.
    :ivar entry_content_parser: Feed URL.

    """
    def __init__(self,
                 feed_url,
                 auto_open=False,
                 entry_content_parser=None):
        """Constructor.

        :param feed_url: Feed URL.
        :param auto_open: Feed URL.
        :param entry_content_parser: Feed URL.
        :type feed_url: str
        :type auto_open: bool
        :type entry_content_parser: function

        """
        self.feed_url = feed_url
        self.reset()
        if auto_open == True:
            self.open()
            
        if entry_content_parser is not None:
            self.entry_content_parser = entry_content_parser
        else:
            self.entry_content_parser = lambda content: content


    def reset(self):
        """Resets state so that parsing can commence.

        """
        self.feed = None
        self.entries = None
        self.entry_count = 0
        self.entry_id = 0
        self.entry = None


    def open(self):
        """Opens feed in readiness for reading.

        """
        if self.feed is not None:
            self.reset()
        parser = feedparser.parse(self.feed_url)
        self.entries = parser.entries
        self.entry_count = len(parser.entries)
        self.feed = parser.feed


    def read(self, onread_callback):
        """Reads next entry within feed collection.

        :param onread_callback: Function to invoke when a feed entry is read.
        :type onread_callback: function 

        """
#        try:
        # Set entry id.
        self.entry_id += 1
        self.entry = self.entries[self.entry_id - 1]

        # Set entry url.
        entry_url = self.entry['links'][0].href

        # TODO place this on queue rather than processing directly.
        # Process entry content (if not already processed).
        if dao.get_ingest_url(entry_url) is None:
            # Notify.
            rt.log("****************************************************************")
            rt.log("[Feed reader ingesting :: {0} of {1}] Target :: {2}".format(self.entry_id, self.entry_count, entry_url))

            # Download.
            http_request = urllib2.Request(entry_url)
            http_response = urllib2.urlopen(http_request)
            entry_content = http_response.read()

            # Process.
            if self.entry_content_parser is not None:
                entry_content = self.entry_content_parser(entry_content)
            onread_callback(entry_url, entry_content)

            # Remember.
            session.insert(IngestURL(URL=entry_url), False)

            # Persist.
            session.commit()

#        except Exception as e:
#            try:
#                session.rollback()
#            except:
#                pass
#            rt.log("FEED READER EXCEPTION :: ERR={0}".format(e))


    def can_read(self):
        """Determines whether another entry can be read.

        """
        return self.entry_count > self.entry_id



class FeedIngestorBase(IngestorBase):
    """Base class for all feed ingestors.
    
    :ivar endpoint: Feed endpoint.
    :ivar project: Project with which feed is associated.
    :ivar ontology: Name of ontology with which feed entries are associated with.
    :ivar language: Language with which feed is associated.
    :ivar url_parser: Function for parsing feed url's.
    :ivar content_parser: Function for parsing feed content.

    """
    def __init__(self,
                 endpoint,
                 project,
                 ontology,
                 language=pyesdoc.ESDOC_DEFAULT_LANGUAGE,
                 content_parser=None):
        """Constructor.

        :param endpoint: Feed endpoint.
        :type endpoint: esdoc_api.models.IngestEndpoint

        :param project: Project with which feed is associated.
        :type project: str

        :param ontology: Name of ontology with which feed entries are associated with.
        :type ontology: str

        :param language: Language with which feed is associated.
        :type language: str

        :param url_parser: Function for parsing feed url's.
        :type url_parser: function

        :param content_parser: Function for parsing feed content.
        :type content_parser: function 
        
        """
        super(FeedIngestorBase, self).__init__(endpoint,
                                               project,
                                               ontology,
                                               language)
        self.entry_content_parser = content_parser
        

    def ingest(self):
        """Executes ingest process.
        
        """
        # Open feed.
        fr = FeedReader(self.ingest_url,
                        auto_open = True,
                        entry_content_parser = self.entry_content_parser)

        # N.B. : uncomment when testing to avoid ingesting entire feed.
        #self.max_ingest_count = 1
        self.max_ingest_count = fr.entry_count

        # Read feed.
        while self.can_ingest() and fr.can_read():
            fr.read(self.on_ingest_callback)

        # Invoke feed parsed callback.
        if hasattr(self, 'on_feed_ingested'):
            self.on_feed_ingested()
            

    def on_ingest_callback(self, url, content):
        """Callback invoked when feed reader reads an entry.
        
        :param url: Feed entry URL.
        :param content: Feed entry content.
        :type url: str
        :type content: str
        
        """
        self.increment_count()
        
        rt.log("{0} INGESTOR :: INGESTING FEED ENTRY :: {1}.".format(self.name.upper(), url))

        self.ingest_feed_entry(content)


    @abstractmethod
    def ingest_feed_entry(self, content):
        """Ingests feed entry currently being processed.

        :param content: Feed entry content.
        :type content: str
        
        """
        pass


    def set_doc_representation(self, document):
        """Create document representation.

        :param document: Document being processed.
        :type document: esdoc_api.models.Document

        """
        # Encode.
        encoding = pyesdoc.ESDOC_ENCODING_JSON
        repr = pyesdoc.encode(document.as_obj, encoding)

        # Assign representation to document.
        utils.create_doc_representation(document,
                                        self.ontology,
                                        self.get_encoding(encoding),
                                        self.language,
                                        unicode(repr))


    def _create_doc(self, etree, nsmap, doc):
        """Creates a document.

        :param etree: Document xml etree.
        :type etree: lxml.etree
        
        :param nsmap: Document xml namespace map.
        :type nsmap: dict

        :param doc: pyesdoc document representation.
        :type doc: pyesdoc.object
        
        """
        # Create document.
        document = utils.create_doc(doc, self.project, self.endpoint)

        # Create document representation.
        self.set_doc_representation(document)
        
        # Create document summary.
        utils.create_doc_summary(document, self.language)
        
        # Create document external ID (i.e. simulation id).
        utils.create_doc_external_ids(document, first_only=True)

        # Print for debugging.
        rt.log("CREATED DOC :: T={0} UID={1} V={2} ID={3}.".format(
            document.Type, document.UID, document.Version, document.ID))

        return document
    

    def on_doc_decoded(self, doc, etree, nsmap):
        """On document decoded handler.

        :param doc: Deserialized pyesdoc document representation.
        :type doc: python object

        :param etree: Document XML.
        :type etree: lxml.etree

        :param nsmap: Document XML namespaces.
        :type nsmap: dict

        """
        pass


    def ingest_document(self, etree, nsmap, parent=None):
        """Ingests a document.

        :param etree: Document xml etree.
        :type etree: lxml.etree

        :param nsmap: Document xml namespace map.
        :type nsmap: dict

        :param parent: Parent pyesdoc instance.
        :type parent: object

        """
        # Decode.
        doc = pyesdoc.decode(etree, pyesdoc.METAFOR_CIM_XML_ENCODING)

        # Assign doc attributes.
        doc.doc_info.project = str(self.project.Name)
        doc.doc_info.source = str(self.endpoint.MetadataSource)
        doc.doc_info.type = doc.__class__.type_key
        if parent is not None:
            doc.doc_info.institute = parent.doc_info.institute
    
        # Call post decoding handler.
        self.on_doc_decoded(doc, etree, nsmap)

        # Retrieve.
        document = utils.get_doc_by_obj(self.project.ID, doc)

        # Create when necessary.
        if document is None:
            document = self._create_doc(etree, nsmap, doc)

        return document
