"""
.. module:: esdoc_api.db.ingest.base_ingestor.py
   :platform: Unix, Windows
   :synopsis: Base class for all ingestors.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from abc import ABCMeta
from abc import abstractmethod

import datetime

from .. import (
    dao,
    utils
    )
from .. models import (
    DocumentEncoding,
    INGEST_STATE_COMPLETE_ID,
    INGEST_STATE_ERROR_ID,
    INGEST_STATE_RUNNING_ID,
    IngestHistory,
    Institute,
    Project
    )
import esdoc_api.lib.utils.runtime as rt



class IngestorBase(object):
    """Base class for all ingestors.

    :ivar endpoint: Ingest endpoint.
    :ivar project: Project with which endpoint is associated.
    :ivar ontology: Name of ontology with which feed entries are associated with.
    :ivar language: Language with which endpoint is associated.
    
    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self,
                 endpoint,
                 project,
                 ontology,
                 language):
        """Constructor.

        :param endpoint: Ingest endpoint.
        :type endpoint: esdoc_api.db.models.IngestEndpoint

        :param project: Project with which endpoint is associated.
        :type project: str

        :param ontology: Name of ontology with which feed entries are associated with.
        :type ontology: str

        :param language: Language with which endpoint is associated.
        :type language: str
        
        """
        self.project = dao.get_by_name(Project, project)
        self.ontology = dao.get_doc_ontology(ontology)
        self.language = dao.get_doc_language(language)
        self.encodings = dao.get_all(DocumentEncoding)
        self.institutes = dao.get_all(Institute)
                
        self.history = utils.create(IngestHistory)
        self.history.StartDateTime = datetime.datetime.now()
        self.history.Endpoint_ID = endpoint.ID
        self.history.State_ID = INGEST_STATE_RUNNING_ID
        self.ingested_count = 0
        self.__max_ingest_count = 0
        self.endpoint = endpoint
        

    @property
    def name(self):
        """Gets ingestor name for use in debugging."""
        return self.ingestor_type

    @property
    def ingestor_type(self):
        """The ingestor type (maps to the ingestor)."""
        return self.endpoint.IngestorType

    @property
    def ingest_url(self):
        """The ingest URL."""
        return self.endpoint.IngestURL

    @property
    def max_ingest_count(self):
        """The maximum allowed ingest count."""
        return self.__max_ingest_count
    

    @max_ingest_count.setter
    def max_ingest_count(self, value):
        """The maximum allowed ingest count."""
        # Defensive progamming.
        if value < 0:
            rt.throw("Max ingest count must be greater than or equal to zero.")
        # Assign max ingest count once - this supports unit test scenarios.
        if self.__max_ingest_count == 0:
            self.__max_ingest_count = value


    def get_encoding(self, encoding):
        """Returns document encoding entity from cached collection.

        :param encoding: Feed entry encoding.
        :type encoding: str
        
        :returns: Encoding type.
        :rtype: esdoc_api.db.models.DocumentEncoding

        """
        encoding = encoding.lower()
        for e in self.encodings:
            if e.Encoding == encoding:
                return e
            
        return None


    def get_institute(self, institute):
        """Returns institute entity from cached collection.

        :param institute: Feed entry institute code.
        :type institute: str
        
        :returns: Institute type.
        :rtype: esdoc_api.db.models.Institute

        """
        for i in self.institutes:
            if isinstance(institute, str) and \
               i.Name.lower() == institute.lower():
                return i
            elif isinstance(institute, int) and \
                i.ID == institute:
                return i
            
        return None


    def can_ingest(self):
        """Determines whether ingestion can take place.
        
        """
        # False if reached limit.
        if self.ingested_count >= self.__max_ingest_count:
            return False
        
        # All tests have passed therefore return true.
        return True


    def increment_count(self):
        """Increments count in readiness for next entry.

        """
        # Defensive programming.
        if self.can_ingest() == False:
            rt.throw("Ingest limits have been reached")

        self.ingested_count = self.ingested_count + 1


    def close(self, error=None):
        """Close ingestor and set context info accordingly.

        :param error: Processing error message.
        :type error: str

        """
        if error is None:
            self.history.State_ID = INGEST_STATE_COMPLETE_ID
        else:
            self.history.State_ID = INGEST_STATE_ERROR_ID
            self.history.ErrorMessage = str(error)[:1023]
        self.history.Count = self.ingested_count
        self.history.EndDateTime = datetime.datetime.now()
        self.history.TimeInMS = self.history.EndDateTime.microsecond - \
                                self.history.StartDateTime.microsecond


    @abstractmethod
    def ingest(self):
        """Executes ingest process.
        
        """
        pass



    