"""
.. module:: esdoc_api.lib.db.ingestion.base_ingestor
   :platform: Unix, Windows
   :synopsis: Base class for all ingestors.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from abc import ABCMeta
from abc import abstractmethod

import datetime

from esdoc_api.lib.utils.cim_exception import CIMException
from esdoc_api.lib.pycim.cim_constants import *
from esdoc_api.models.entities.document_encoding import DocumentEncoding
from esdoc_api.models.entities.document_language import DocumentLanguage
from esdoc_api.models.entities.document_schema import DocumentSchema
from esdoc_api.models.entities.ingest_endpoint import IngestEndpoint
from esdoc_api.models.entities.ingest_history import IngestHistory
from esdoc_api.models.entities.ingest_state import *
from esdoc_api.models.entities.project import Project



class IngestorBase(object):
    """Base class for all ingestors.

    :ivar endpoint: Ingest endpoint.
    :ivar project: Project with which endpoint is associated.
    :ivar schema: CIM schema with which endpoint is associated.
    :ivar language: Language with which endpoint is associated.
    
    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self, endpoint, project, schema, language):
        """Constructor.

        :param endpoint: Ingest endpoint.
        :param project: Project with which endpoint is associated.
        :param schema: CIM schema with which endpoint is associated.
        :param language: Language with which endpoint is associated.
        :type endpoint: esdoc_api.models.entities.IngestEndpoint
        :type project: str
        :type schema: str
        :type language: str
        
        """
        self.ingest_project = project
        self.ingest_schema = schema
        self.ingest_language = language
        self.cim_project = Project.retrieve(self.ingest_project)
        self.cim_schema = DocumentSchema.retrieve(self.ingest_schema)
        self.cim_language = DocumentLanguage.retrieve(self.ingest_language)
        self.cim_encodings = DocumentEncoding.get_all()
        self.history = IngestHistory()
        self.history.Endpoint = endpoint
        self.history.set_state(EXECUTION_STATE_RUNNING)
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
            raise CIMException(u"Max ingest count must be greater than or equal to zero.")
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
            raise CIMException(u"Ingest limits have been reached")

        self.ingested_count = self.ingested_count + 1


    def close(self, error=None):
        """Close ingestor and set context info accordingly.

        :param error: Processing error message.
        :type error: str

        """
        if error is None:
            self.history.set_state(EXECUTION_STATE_COMPLETE)
        else:
            self.history.set_state(EXECUTION_STATE_ERROR)
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



    