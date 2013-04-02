"""
A set of domain entity unit tests.
"""

# Module imports.
import unittest
from cim_components_test.entity.entity_tester import EntityTester




class TestIngestRegistration(unittest.TestCase):
    """
    Encapsulates domain entity unit tests.
    """

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_import(self):
        from esdoc_api.models.entities.cim.ingest_registration import IngestRegistration


    def test_create(self):
        from esdoc_api.models.entities.cim.ingest_registration import IngestRegistration
        EntityTester.do_tests(IngestRegistration)
