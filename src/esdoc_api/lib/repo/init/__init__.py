"""
.. module:: esdoc_api.lib.repo.init.__init__.py
   :platform: Unix
   :synopsis: Repository setup entry point.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.lib.repo.init.populate_document_encoding import populate_document_encoding 
from esdoc_api.lib.repo.init.populate_document_language import populate_document_language 
from esdoc_api.lib.repo.init.populate_document_ontology import populate_document_ontology
from esdoc_api.lib.repo.init.populate_document_type import populate_document_type
from esdoc_api.lib.repo.init.populate_facet import populate_facet
from esdoc_api.lib.repo.init.populate_facet_relation_type import populate_facet_relation_type
from esdoc_api.lib.repo.init.populate_facet_type import populate_facet_type
from esdoc_api.lib.repo.init.populate_ingest_endpoint import populate_ingest_endpoint
from esdoc_api.lib.repo.init.populate_ingest_state import populate_ingest_state
from esdoc_api.lib.repo.init.populate_institute import populate_institute
from esdoc_api.lib.repo.init.populate_project import populate_project
import esdoc_api.lib.utils.runtime as rt



# Module exports.
__all__ = [
    'execute'
]



# Set repository population functions to be invoked.
# N.B. order matters.
_populators = [
    populate_document_encoding,
    populate_document_language,
    populate_document_ontology,
    populate_document_type,
    populate_facet_type,
    populate_facet_relation_type,
    populate_institute,
    populate_ingest_endpoint,
    populate_ingest_state,
    populate_project,
    populate_facet,
]


def execute():
    """Executes repo setup.

    """
    rt.log("REPOSITORY POPULATION BEGINS")

    for f in _populators:
        rt.log("ES-DOC API :: REPOSITORY POPULATION :: {0}".format(f.__name__))
        f()

    rt.log("REPOSITORY POPULATION ENDS")

