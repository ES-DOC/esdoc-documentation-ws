"""
A set of domain entity unit tests.
"""

# Module imports.
import unittest
from cim_components_test.entity.entity_tester import EntityTester



class TestInstitute(unittest.TestCase):
    """
    Encapsulates domain entity unit tests.
    """

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_import(self):
        from esdoc_api.models.entities.cim.institute import Institute


    def test_create(self):
        from esdoc_api.models.entities.cim.institute import Institute
        EntityTester.do_tests(Institute)


    def test_query_all(self):
        from esdoc_api.models.entities.cim.institute import Institute

        q = Institute.query
        collection = q.all()

        assert collection is not None
        assert len(collection) > 10


    def test_query_one(self):
        from esdoc_api.models.entities.cim.institute import Institute

        q = Institute.query.filter(Institute.Name==u"IPSL")
        instance = q.one()

        assert instance is not None
        assert isinstance(instance, Institute)
