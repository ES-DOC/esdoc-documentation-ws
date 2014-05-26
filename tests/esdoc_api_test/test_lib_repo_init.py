"""
.. module:: esdoc_api_test.test_repo_init.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Repository initialisation functional tests.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""

# Module imports.
import esdoc_api.db.dao as dao
import esdoc_api.db.models as models
import esdoc_api_test.utils as tu
import esdoc_api.pyesdoc as pyesdoc
from esdoc_api.lib.utils.cim_v1 import ACTIVE_TYPES
from esdoc_api.db.ingest import INGESTOR_KEYS



def test_populate_document_encoding():
    all = dao.get_all(models.DocumentEncoding)
    tu.assert_iter(all, len(pyesdoc.ESDOC_ENCODINGS))
    tu.assert_in_collection(all, "Encoding", pyesdoc.ESDOC_ENCODINGS)


def test_populate_document_language():
    all = dao.get_all(models.DocumentLanguage)
    tu.assert_iter(all, 139)
    tu.assert_in_collection(all, "Code", ["en", "ar", "de", "fr", "es", "zh"])


def test_populate_document_ontology():
    all = dao.get_all(models.DocumentOntology)
    tu.assert_iter(all, len(pyesdoc.ESDOC_ONTOLOGIES))
    tu.assert_in_collection(all, "Name", pyesdoc.ESDOC_ONTOLOGIES)
    cim_v1_ontology = [i for i in all if i.Name == "cim" and i.Version == "1"][0]
    tu.assert_str(cim_v1_ontology.FullName, "cim-v1")


def test_populate_document_type():
    all = dao.get_all(models.DocumentType)
    tu.assert_iter(all, len(pyesdoc.ACTIVE_TYPES))
    tu.assert_in_collection(all, "Name", (i.upper() for i in ACTIVE_TYPES))


def test_populate_facet():
    all = dao.get_all(models.Facet)
    tu.assert_iter(all, 29)
    tu.assert_in_collection(all, "Key", ["IPSL", "MPI-M", "NCAR", "BADC"])


def test_populate_facet_relation_type():
    all = dao.get_all(models.FacetRelationType)
    tu.assert_iter(all, len(models.FACET_RELATION_TYPES))
    tu.assert_in_collection(all, "Name", models.FACET_RELATION_TYPES)


def test_populate_facet_type():
    all = dao.get_all(models.FacetType)
    tu.assert_iter(all, len(models.FACET_TYPES))
    tu.assert_in_collection(all, "Name", models.FACET_TYPES)


def test_populate_ingest_endpoint():
    all = dao.get_all(models.IngestEndpoint)
    tu.assert_iter(all, len(INGESTOR_KEYS))
    tu.assert_in_collection(all, "IngestorType", INGESTOR_KEYS)


def test_populate_ingest_state():
    all = dao.get_all(models.IngestState)
    tu.assert_iter(all, len(models.INGEST_STATES))
    tu.assert_in_collection(all, "Name", models.INGEST_STATES)


def test_populate_institute():
    all = dao.get_all(models.Institute)
    tu.assert_iter(all, 29)
    tu.assert_in_collection(all, "Name", ["IPSL", "MPI-M", "NCAR", "BADC"])


def test_populate_project():
    all = dao.get_all(models.Project)
    tu.assert_iter(all, 3)
    tu.assert_in_collection(all, "Name", ["CMIP5", "DCMIP-2012", "QED-2013"])

