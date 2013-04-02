"""
.. module:: esdoc_api.lib.db.ingestion.do_ingest
   :platform: Unix, Windows
   :synopsis: Supports debugging of ingestion against set of specific url's.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import datetime
import urllib2

from esdoc_api.lib.db.pgres.connect import *
from esdoc_api.lib.db.ingestion.factory import create_ingestor
from esdoc_api.models.entities.ingest_endpoint import IngestEndpoint


# Endpoint = CMIP5 Questionnaire
_EP_01 = 'http://q.cmip5.ceda.ac.uk/feeds/cmip5/all'

# Simulation : ERR = null value in column "Project_ID" violates not-null constraint.
_EP_01_URL_01 = ' http://q.cmip5.ceda.ac.uk/cmip5/simulation/d2113c12-ccff-11e1-ae50-00163e9152a5/1/'

# Simulation (with ensemble): ERR = null value in column "Project_ID" violates not-null constraint.
_EP_01_URL_02 = 'http://q.cmip5.ceda.ac.uk/cmip5/simulation/f134bbba-40f9-11e1-a594-00163e9152a5/1'

# Experiment with document version as a document attribute rather than a documentVersion element.
_EP_01_URL_03 = "http://q.cmip5.ceda.ac.uk/cmip5/experiment/76f85a8a-4830-11e1-8ba0-00163e9152a5/2"

# Model component with facets.
_EP_01_URL_04 = " http://q.cmip5.ceda.ac.uk/cmip5/component/03c6cbaa-fd27-11df-a88e-00163e9152a5/5"

# Old experiment document.
_EP_01_URL_05 = "http://q.cmip5.ceda.ac.uk/cmip5/experiment/581acb8e-4830-11e1-9409-00163e9152a5/1"

# New experiment document.
_EP_01_URL_06 = "http://q.cmip5.ceda.ac.uk/cmip5/experiment/2960be30-8876-11e1-b0c4-0800200c9a66/2"

# GFDL simulation document with invalid DRS tag.
_EP_01_URL_07 = "http://q.cmip5.ceda.ac.uk/cmip5/simulation/7800a084-6169-11e1-bd49-00163e9152a5/2/"



# Endpoint = CMIP5 QC.
_EP_02 = 'http://cera-www.dkrz.de/WDCC/CMIP5/feed'
_EP_02_URL_01 = "http://cera-www.dkrz.de/WDCC/CMIP5/downloadAtomXml?id=26494"



def _ingest(ep_url, content_url):
    """Launches an ingest against a specific url.

    :param ep_url: Ingest endpoint URL.
    :param content_url: Ingest content URL.
    :type ep_url: str
    :type content_url: str
    
    """
    print "****************************************************************"
    print "Processing :: EP = {0} URL = {1}".format(ep_url, content_url)
    
    # Get ingestor.
    endpoint = IngestEndpoint.retrieve_by_url(ep_url)
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
    except Exception as e:
        session.rollback()
        print "FEED READER EXCEPTION :: ERR={0}".format(e)
    finally:
        print "Processed :: EP = {0} URL = {1}".format(ep_url, content_url)
        print "****************************************************************"


if __name__ == "__main__":
    '''Standalone mode entry point.'''
    _ingest(_EP_01, _EP_01_URL_04)

