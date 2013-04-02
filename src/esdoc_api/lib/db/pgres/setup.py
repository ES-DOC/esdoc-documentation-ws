"""Sets up CIM postgres database.

"""

# Module imports.
from esdoc_api.lib.db.pgres.connect import *
from esdoc_api.lib.db.pgres.populate_document_encoding import populate_document_encoding
from esdoc_api.lib.db.pgres.populate_document_language import populate_document_language
from esdoc_api.lib.db.pgres.populate_document_schema import populate_document_schema
from esdoc_api.lib.db.pgres.populate_document_type import populate_document_type
from esdoc_api.lib.db.pgres.populate_facet import populate_facet
from esdoc_api.lib.db.pgres.populate_facet_type import populate_facet_type
from esdoc_api.lib.db.pgres.populate_facet_relation_type import populate_facet_relation_type
from esdoc_api.lib.db.pgres.populate_ingest_endpoint import populate_ingest_endpoint
from esdoc_api.lib.db.pgres.populate_ingest_state import populate_ingest_state
from esdoc_api.lib.db.pgres.populate_institute import populate_institute
from esdoc_api.lib.db.pgres.populate_project import populate_project


def populate():
    # Set population functions (order matters!).
    fns = [
        populate_document_encoding,
        populate_document_schema,
        populate_document_type,
        populate_document_language,
        populate_facet_type,
        populate_facet_relation_type,
        populate_institute,
        populate_ingest_endpoint,
        populate_ingest_state,
        populate_project,
        populate_facet,
    ]

    # Execute population functions.
    print "ES-DOC PYCIM POSTGRES DB PROPULATION BEGINS"
    for fn in fns:
        print "ES-DOC PYCIM POSTGRES DB PROPULATION :: {0}".format(fn.__name__)
        fn()
        session.commit()
    print "CIM POSTGRES DB PROPULATION ENDS"
    

# Create db tables.
create_all()

# Populate db tables.
populate()

