"""
.. module:: esdoc_api.lib.repo.ingest.base_ingestor.py
   :platform: Unix, Windows
   :synopsis: Base class for all ingestors.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from abc import ABCMeta
from abc import abstractmethod

import datetime

import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.utils as utils
import esdoc_api.lib.utils.runtime as rt
from esdoc_api.models import (
    DocumentEncoding,
    INGEST_STATE_COMPLETE_ID,
    INGEST_STATE_ERROR_ID,
    INGEST_STATE_RUNNING_ID,
    IngestHistory,
    Project
    )



class IngestorBase(object):
    """Base class for all ingestors.

    :ivar endpoint: Ingest endpoint.
    :ivar project: Project with which endpoint is associated.
    :ivar ontology_name: Name of ontology with which feed entries are associated with.
    :ivar ontology_version: Version of ontology with which feed entries are associated with.
    :ivar language: Language with which endpoint is associated.
    
    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self,
                 endpoint,
                 project,
                 ontology_name,
                 ontology_version,
                 language):
        """Constructor.

        :param endpoint: Ingest endpoint.
        :type endpoint: esdoc_api.models.IngestEndpoint

        :param project: Project with which endpoint is associated.
        :type project: str

        :param ontology_name: Name of ontology with which feed entries are associated with.
        :type ontology_name: str

        :param ontology_version: Version of ontology with which feed entries are associated with.
        :type ontology_version: str

        :param language: Language with which endpoint is associated.
        :type language: str
        
        """
        self.project = dao.get_by_name(Project, project)
        self.ontology = dao.get_document_ontology(ontology_name, ontology_version)
        self.language = dao.get_document_language(language)
        self.encodings = dao.get_all(DocumentEncoding)
                
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



    