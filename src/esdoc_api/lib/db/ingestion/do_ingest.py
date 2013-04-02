"""
.. module:: esdoc_api.lib.db.ingestion.do_ingest
   :platform: Unix, Windows
   :synopsis: Executes ingestion against set of pending endpoints.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import datetime

from esdoc_api.lib.db.pgres.connect import *
from esdoc_api.lib.utils.cim_exception import CIMException
from esdoc_api.lib.db.ingestion.factory import create_ingestor



def execute_ingestion():
    """Launches the set of pending ingest jobs.
    
    """
    print "***************** INGESTION START *****************"
    print "   STARTED @ {0}.".format(datetime.datetime.now())
    print "***************** INGESTION START *****************"

    # Get all active ingestions.
    active = IngestEndpoint.get_active()
    print "Active ingestion endpoints = {0}".format(len(active))

    # For each pending, create ingestor & ingest.
    ingestor = None
    for endpoint in active:
        # Create ingestor.
        ingestor = create_ingestor(endpoint)
        session.commit()

        # Inform.
        print '****************************************************************'
        print "Ingesting :: URL={0}".format(ingestor.ingest_url)

        try:
            # Ingest & persist.
            ingestor.ingest(session)
            ingestor.close()
            session.commit()

            # Inform.
            print "Ingested :: URL={0}".format(ingestor.ingest_url)
            print '****************************************************************'
            
        except Exception as e:
            # Rollback inner transaction.
            try:
                session.rollback()
            except:
                pass

            # Update ingestion history.
            if ingestor is not None:
                try:
                    ingestor.close(CIMException(str(e)))
                    session.commit()
                except:
                    pass
            
            # Inform.
            print "INGEST ERROR :: {0}.".format(str(e))


    print "***************** INGESTION END *******************"
    print "   COMPLETED @ {0}.".format(datetime.datetime.now())
    print "***************** INGESTION END *******************"


if __name__ == "__main__":
    '''Standalone mode entry point.'''
    execute_ingestion()
