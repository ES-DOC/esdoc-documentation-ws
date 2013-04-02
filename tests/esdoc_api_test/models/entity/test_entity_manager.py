"""
A set of unit tests over the entity manager.
"""

# Module imports.
import unittest
from esdoc_api.models.entities.entity_types import *
from esdoc_api.models.entities.entity_manager import EntityManager


class TestEntityManager(unittest.TestCase):
    """
    Encapsulates domain entity unit tests.
    """

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_instantiation_cim_ingest_history(self):
        assert EntityManager(IngestHistory) is not None

    def test_instantiation_cim_ingest_registration(self):
        assert EntityManager(IngestRegistration) is not None

    def test_instantiation_cim_ingest_source(self):
        assert EntityManager(IngestSource) is not None

    def test_instantiation_cim_ingest_state(self):
        assert EntityManager(IngestState) is not None

    def test_instantiation_cim_institute(self):
        assert EntityManager(Institute) is not None

