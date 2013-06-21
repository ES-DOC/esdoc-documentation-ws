"""
.. module:: esdoc_api.lib.db.ingestion.base_ingestor_from_feed
   :platform: Unix, Windows
   :synopsis: Base class for all feed ingestors.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from abc import abstractmethod
import urllib2

import feedparser
from lxml import etree as et

from esdoc_api.lib.db.ingestion.base_ingestor import IngestorBase
from esdoc_api.lib.pyesdoc.utils.ontologies import *
from esdoc_api.lib.pyesdoc import (
    decode as pyesdoc_decoder,
    encode as pyesdoc_encoder
    )
from esdoc_api.models.entities import *
from esdoc_api.models.daos.document_representation import assign as assign_representation



class FeedReader(object):
    """Atom/RSS feed reader - wraps feedparser.

    :ivar feed_url: Feed URL.
    :ivar auto_open: Feed URL.
    :ivar entry_url_parser: Feed URL.
    :ivar entry_content_parser: Feed URL.

    """
    def __init__(self,
                 feed_url,
                 auto_open=False,
                 entry_url_parser=None,
                 entry_content_parser=None):
        """Constructor.

        :param feed_url: Feed URL.
        :param auto_open: Feed URL.
        :param entry_url_parser: Feed URL.
        :param entry_content_parser: Feed URL.
        :type feed_url: str
        :type auto_open: bool
        :type entry_url_parser: function
        :type entry_content_parser: function

        """
        self.feed_url = feed_url
        self.reset()
        if auto_open == True:
            self.open()
        self.entry_url_parser = entry_url_parser
        self.entry_content_parser = entry_content_parser


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


    def read(self, onread_callback, session):
        """Reads next entry within feed collection.

        :param onread_callback: Function to invoke when a feed entry is read.
        :param session: Db session context.
        :type onread_callback: function 
        :param session: elixir.Session

        """
        try:
            # Set entry id.
            self.entry_id += 1
            self.entry = self.entries[self.entry_id - 1]

            # Set entry url.
            entry_url = self.entry['links'][0].href
            if self.entry_url_parser is not None:
                entry_url = self.entry_url_parser(entry_url)

            # TODO place this on queue rather than processing directly.
            # Process entry content (if not already processed).
            if IngestURL.retrieve(entry_url) is None:
                # Notify.
                print "****************************************************************"
                print "[Feed reader ingesting :: {0} of {1}] Target :: {2}".format(self.entry_id, self.entry_count, entry_url)

                # Download.
                http_request = urllib2.Request(entry_url)
                http_response = urllib2.urlopen(http_request)
                entry_content = http_response.read()

                # Process.
                if self.entry_content_parser is not None:
                    entry_content = self.entry_content_parser(entry_content)
                onread_callback(entry_url, entry_content)

                # Remember.
                IngestURL.create(entry_url)

                # Persist.
                session.commit()

        except Exception as e:
            try:
                session.rollback()
            except:
                pass
            print "FEED READER EXCEPTION :: ERR={0}".format(e)


    def can_read(self):
        """Determines whether another entry can be read.

        """
        return self.entry_count > self.entry_id



class FeedIngestorBase(IngestorBase):
    """Base class for all feed ingestors.
    
    :ivar endpoint: Feed endpoint.
    :ivar project: Project with which feed is associated.
    :ivar schema: CIM schema with which feed is associated.
    :ivar language: Language with which feed is associated.
    :ivar url_parser: Function for parsing feed url's.
    :ivar content_parser: Function for parsing feed content.

    """
    def __init__(self,
                 endpoint,
                 project,
                 schema,
                 language=CIM_DEFAULT_LANGUAGE,
                 url_parser=None,
                 content_parser=None):
        """Constructor.

        :param endpoint: Feed endpoint.
        :param project: Project with which feed is associated.
        :param schema: CIM schema with which feed is associated.
        :param language: Language with which feed is associated.
        :param url_parser: Function for parsing feed url's.
        :param content_parser: Function for parsing feed content.
        :type endpoint: esdoc_api.models.entities.IngestEndpoint
        :type project: str
        :type schema: str
        :type language: str
        :type url_parser: function
        :type content_parser: function 
        
        """
        super(FeedIngestorBase, self).__init__(endpoint, project, schema, language)
        self.entry_url_parser = url_parser
        self.entry_content_parser = content_parser
        

    def ingest(self, session):
        """Executes ingest process.
        
        :param session: Db session context.
        :param session: elixir.Session

        """
        # Open feed.
        fr = FeedReader(self.ingest_url,
                        auto_open = True,
                        entry_url_parser = self.entry_url_parser,
                        entry_content_parser = self.entry_content_parser)

        # N.B. : uncomment when testing to avoid ingesting entire feed.
        #self.max_ingest_count = 1
        self.max_ingest_count = fr.entry_count

        # Read feed.
        while self.can_ingest() and fr.can_read():
            fr.read(self.on_ingest_callback, session)

        # Invoke feed parsed callback.
        self.on_feed_ingested()
            

    def on_ingest_callback(self, url, content):
        """Callback invoked when feed reader reads an entry.
        
        :param url: Feed entry URL.
        :param content: Feed entry content.
        :type url: str
        :type content: str
        
        """
        self.increment_count()
        
        print u"{0} INGESTOR :: INGESTING FEED ENTRY :: {1}.".format(self.name.upper(), url)

        self.ingest_feed_entry(content)


    @abstractmethod
    def ingest_feed_entry(self, content):
        """Ingests feed entry currently being processed.

        :param content: Feed entry content.
        :type content: str
        
        """
        pass
    

    @abstractmethod
    def on_feed_ingested(self):
        """Callback invoked when a feed has been ingested.

        """
        pass


    def get_cim_encoding(self, encoding):
        """Returns cim encoding entity from cached collection.

        :param encoding: Feed entry encoding.
        :type encoding: str
        :returns: Encoding type.
        :rtype: esdoc_api.models.entities.DocumentEncoding

        """
        encoding = encoding.lower()
        for e in self.cim_encodings:
            if e.Encoding == encoding:
                return e
        return None


    def set_document_representations(self, document, etree):
        """Create document representations.

        :param document: Document being processed.
        :param etree: Document xml etree.
        :type document: esdoc_api.models.entities.Document
        :type etree: lxml.etree

        """
        self.set_document_representation(document, CIM_ENCODING_JSON)
        doc_xml = et.tostring(etree).decode('UTF-8','strict')
        self.set_document_representation(document, CIM_ENCODING_XML, doc_xml)

    
    def set_document_representation(self, document, encoding, representation=None):
        """Create document representation.

        :param document: Document being processed.
        :param encoding: Encoding type.
        :param representation: Document representation.
        :type document: esdoc_api.models.entities.Document
        :type encoding: esdoc_api.models.entities.DocumentEncoding
        :type representation: unicode
        
        """
        # Encode (if necessary).
        if representation is None:
            representation = pyesdoc_encoder(document.as_obj,
                                             self.cim_schema.Version,
                                             encoding)

        # Assign representation to document.
        assign_representation(document,
                              self.cim_schema,
                              self.get_cim_encoding(encoding),
                              self.cim_language,
                              representation)


    def set_document_indexes(self, document):
        """Create document search indexes.

        :param document: Document being processed.
        :type document: esdoc_api.models.entities.Document

        """
        DocumentByExternalID.create(document, first_only=True)
                                      

    def create_document(self, etree, nsmap, as_obj):
        """Creates a cim document.

        :param etree: Document xml etree.
        :type etree: lxml.etree
        
        :param nsmap: Document xml namespace map.
        :type nsmap: dict

        :param as_obj: pyesdoc document representation.
        :type as_obj: pyesdoc.object
        
        """
        # Create document, representations, summary.
        document = Document.create(self.cim_project, self.endpoint, as_obj)
        self.set_document_representations(document, etree)
        document.Summaries.append(DocumentSummary.create(document, self.cim_language))

        # Create search indexes.
        self.set_document_indexes(document)

        # Print for debugging.
        print u"CREATED DOC :: T={0} ID={1} UID={2} V={3}.".format(
            document.Type, document.ID, document.UID, document.Version)

        return document
            

    def ingest_document(self, etree, nsmap, on_deserialize=None):
        """Ingests a cim document.

        :param etree: Document xml etree.
        :param nsmap: Document xml namespace map.
        :param on_deserialize: Function to invoke when document has been deserialized.
        :type etree: lxml.etree
        :type nsmap: dict
        :type on_deserialize: function

        """
        # Deserialize.
        as_obj = pyesdoc_decoder(etree, CIM_SCHEMA_1_5, CIM_ENCODING_XML)
    
        # Assign doc info attributes.
        as_obj.cim_info.project = self.cim_project.Name
        as_obj.cim_info.source = self.endpoint.MetadataSource

        # Call post deserialization callback.
        if on_deserialize is not None:
            on_deserialize(as_obj, etree, nsmap)

        # Retrieve / create as appropriate.
        document = Document.retrieve(self.cim_project, as_obj)
        if document is None:
            document = self.create_document(etree, nsmap, as_obj)

        return document
    
