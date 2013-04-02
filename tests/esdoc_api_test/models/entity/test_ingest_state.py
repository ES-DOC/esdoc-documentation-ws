"""
A set of domain entity unit tests over the apps schema.
"""

# Module imports.
import unittest
from cim_components_test.entity.entity_tester import EntityTester


class TestIngestState(unittest.TestCase):
    """
    Encapsulates domain entity unit tests.
    """

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_import(self):
        from esdoc_api.models.entities.cim.ingest_state import IngestState


    def test_create(self):
        from esdoc_api.models.entities.cim.ingest_state import IngestState
        EntityTester.do_tests(IngestState)


    def test_query_all(self):
        from esdoc_api.models.entities.cim.ingest_state import IngestState

        q = IngestState.query
        collection = q.all()

        assert collection is not None
        assert len(collection) == 5


    def test_query_one(self):
        from esdoc_api.models.entities.cim.ingest_state import IngestState

        q = IngestState.query.filter(IngestState.Name==u"QUEUED")
        instance = q.one()

        assert instance is not None
        assert isinstance(instance, IngestState)
        

    def test_query_like(self):
        from esdoc_api.models.entities.cim.ingest_state import IngestState

        q = IngestState.query.filter(IngestState.Name.like(u"%ED"))
        collection = q.all()

        assert collection is not None
        assert len(collection) == 2
        

    def test_query_and(self):
        def do_assert(collection):
            assert collection is not None
            assert len(collection) == 2

        def do_test_generative():
            q = IngestState.query.filter(IngestState.Name.like(u"%ED"))
            q = q.filter(IngestState.Code > 0)
            do_assert(q.all())

        def do_test_chaining_01():
            q = IngestState.query.filter(IngestState.Name.like(u"%ED")).filter(IngestState.Code > 0)
            do_assert(q.all())

        def do_test_chaining_02():
            from sqlalchemy import and_
            q = IngestState.query.filter(and_(IngestState.Name.like(u"%ED"), IngestState.Code > 0))
            do_assert(q.all())

        from esdoc_api.models.entities.cim.ingest_state import IngestState
        do_test_generative()
        do_test_chaining_01()
        do_test_chaining_02()


    def test_query_or(self):
        from sqlalchemy import or_
        from esdoc_api.models.entities.cim.ingest_state import IngestState
        q = IngestState.query.filter(or_(IngestState.Name.like(u"%ED"), IngestState.Code > 400))
        collection = q.all()

        assert collection is not None
        assert len(collection) == 3