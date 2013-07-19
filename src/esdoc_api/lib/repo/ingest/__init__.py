"""
.. module:: esdoc_api.lib.repo.ingest.__init__.py
   :platform: Unix, Windows
   :synopsis: Exposes entry points into ingestion sub-package.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import datetime
import urllib2

import lxml

from esdoc_api.lib.repo.ingest.ingestor_cmip5_quality_control import Ingestor as CMIP5QCIngestor
from esdoc_api.lib.repo.ingest.ingestor_cmip5_questionnaire import Ingestor as CMIP5QuestionnaireIngestor
from esdoc_api.lib.repo.ingest.ingestor_dcmip2012 import Ingestor as DCMIP2012Ingestor
from esdoc_api.lib.repo.ingest.ingestor_qed2013 import Ingestor as QED2013Ingestor
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.utils.runtime as rt



# Collection of supported ingestor keys.
INGESTOR_KEYS = (
    'cmip5q',
    'cmip5qc',
    'dcmip2012',
    'qed2013'
)

# Map of supported ingestor types.
_ingestor_types = {
    'cmip5q' : CMIP5QuestionnaireIngestor,
    'cmip5qc' : CMIP5QCIngestor,
    'dcmip2012' : DCMIP2012Ingestor,
    'qed2013' : QED2013Ingestor
}


def create_ingestor(endpoint):
    """Factory method to instantiate an ingest endpoint ingestor.

    :param endpoint: Ingest endpoint.
    :type endpoint: esdoc_api.models.IngestEndpoint

    """
    if endpoint.IngestorType not in _ingestor_types:
        raise rt.ESDOC_API_Error("Unsupported ingestor :: {0}.".format(type))

    print "Creating ingestor :: {0} (endpoint = {1}).".format(endpoint.IngestorType, endpoint.IngestURL)
    return _ingestor_types[endpoint.IngestorType](endpoint)


def execute():
    """Launches the set of pending ingest jobs.

    """
    print "***************** INGESTION START *****************"
    print "   STARTED @ {0}.".format(datetime.datetime.now())
    print "***************** INGESTION START *****************"

    # Repo connection string.
    _CONNECTION = "postgresql://postgres:Silence107!@localhost:5432/esdoc_api"

    # Start session.
    session.start(_CONNECTION)

    # Get all active ingestions.
    active = dao.get_ingest_endpoints()
    print "Active ingestion endpoints = {0}".format(len(active))

    # For each pending, create ingestor & ingest.
    ingestor = None
    for endpoint in active:
        # Create ingestor.
        ingestor = create_ingestor(endpoint)

        # Inform.
        print '****************************************************************'
        print "Ingesting :: URL={0}".format(ingestor.ingest_url)

        try:
            # Ingest & persist.
            ingestor.ingest()
            ingestor.close()
            session.commit()

            # Inform.
            print "Ingested :: URL={0}".format(ingestor.ingest_url)
            print '****************************************************************'

        except Exception as e:
            raise
        
            # Rollback inner transaction.
            try:
                session.rollback()
            except:
                pass

            # Update ingestion history.
            if ingestor is not None:
                try:
                    ingestor.close(rt.ESDOC_API_Error(e))
                    session.commit()
                except:
                    pass

            # Inform.
            print "INGEST ERROR :: {0}.".format(str(e))


    print "***************** INGESTION END *******************"
    print "   COMPLETED @ {0}.".format(datetime.datetime.now())
    print "***************** INGESTION END *******************"


def ingest_url(ep_url, content_url):
    """Ingests a specific url.

    :param ep_url: Ingest endpoint URL.
    :type ep_url: str

    :type content_url: str
    :param content_url: Ingest content URL.

    """
    print "****************************************************************"
    print "Processing :: EP = {0} URL = {1}".format(ep_url, content_url)

    # Get ingestor.
    endpoint = dao.get_ingest_endpoint(ep_url)
    ingestor = create_ingestor(endpoint)

    # Get content.
    http_request = urllib2.Request(content_url)
    try:
        http_response = urllib2.urlopen(http_request)
        content = http_response.read()
        if hasattr(ingestor, 'parse_entry_content'):
            content = ingestor.parse_entry_content(content)
        ingestor.ingest_feed_entry(content)
        session.commit()
#    except Exception as e:
#        session.rollback()
#        print "FEED READER EXCEPTION :: ERR={0}".format(e)
    finally:
        print "Processed :: EP = {0} URL = {1}".format(ep_url, content_url)
        print "****************************************************************"


def ingest_file(ep_url, content_filepath):
    """Ingests a file.

    :param ep_url: Ingest endpoint URL.
    :type ep_url: str

    :param content_filepath: Ingest content filepath.
    :type content_filepath: str

    """
    print "****************************************************************"
    print "Processing :: EP = {0} FILE = {1}".format(ep_url, content_filepath)

    # Get ingestor.
    endpoint = dao.get_ingest_endpoint(ep_url)
    ingestor = create_ingestor(endpoint)

    # Get content.
    try:
        content = lxml.etree.parse(content_filepath)
        content = lxml.etree.tostring(content).decode('UTF-8','strict')
        if hasattr(ingestor, 'parse_entry_content'):
            content = ingestor.parse_entry_content(content)
        ingestor.ingest_feed_entry(content)
        session.commit()
#    except Exception as e:
#        session.rollback()
#        print "FEED READER EXCEPTION :: ERR={0}".format(e)
    finally:
        print "Processed :: EP = {0} FILE = {1}".format(ep_url, content_filepath)
        print "****************************************************************"
