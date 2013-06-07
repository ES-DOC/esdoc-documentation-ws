"""
.. module:: esdoc_api.lib.db.ingestion.factory
   :platform: Unix, Windows
   :synopsis: Ingestor factory.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.lib.utils.exception import ESDOCAPIException
from esdoc_api.lib.db.ingestion.ingestors.from_cmip5_quality_control import FromCMIP5QualityControlIngestor
from esdoc_api.lib.db.ingestion.ingestors.from_cmip5_questionnaire import FromCMIP5QuestionnaireIngestor
from esdoc_api.lib.db.ingestion.ingestors.from_dcmip2012 import FromDCMIP2012Ingestor



# Supported ingestor types.
_ingestor_types = {
    'cmip5q' : FromCMIP5QuestionnaireIngestor,
    'cmip5qc' : FromCMIP5QualityControlIngestor,
    'dcmip2012' : FromDCMIP2012Ingestor
}


def create_ingestor(endpoint):
    """Instantiates an ingestor to process an ingest endpoint.

    :param endpoint: Ingest endpoint.
    :type endpoint: esdoc_api.models.entities.IngestEndpoint
    
    """
    if endpoint.IngestorType not in _ingestor_types:
        raise ESDOCAPIException(u"Unsupported ingestor :: {0}.".format(type))

    print "Creating ingestor :: {0} (endpoint = {1}).".format(endpoint.IngestorType, endpoint.IngestURL)
    return _ingestor_types[endpoint.IngestorType](endpoint)

