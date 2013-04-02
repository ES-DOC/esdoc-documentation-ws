"""
A set of domain entity unit tests.
"""

# Module imports.
import unittest
from cim_components_test.entity.entity_tester import EntityTester


class TestIngestSource(unittest.TestCase):
    """
    Encapsulates domain entity unit tests.
    """

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_import(self):
        from esdoc_api.models.entities.cim.ingest_source import IngestSource


    def test_create(self):
        from esdoc_api.models.entities.cim.ingest_source import IngestSource
        EntityTester.do_tests(IngestSource)


    def test_query_all(self):
        from esdoc_api.models.entities.cim.ingest_source import IngestSource

        q = IngestSource.query
        collection = q.all()

        assert collection is not None
        assert len(collection) == 4


    def test_query_one(self):
        from esdoc_api.models.entities.cim.ingest_source import IngestSource
        from esdoc_api.models.entities.cim.ingest_source import INGEST_SOURCE_CMIP5_QC

        q = IngestSource.query.filter(IngestSource.Name==INGEST_SOURCE_CMIP5_QC)
        instance = q.one()

        assert instance is not None
        assert isinstance(instance, IngestSource)
