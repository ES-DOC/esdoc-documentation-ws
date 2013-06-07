"""
A set of domain entity unit tests.
"""

# Module imports.
import unittest
from esdoc_api.lib.utils.exception import ESDOCAPIException
from esdoc_api.models.search.search_types import *
from esdoc_api.models.search.search_manager import SearchManager



class TestSearchManager(unittest.TestCase):
    """
    Encapsulates domain entity unit tests.
    """

    def setUp(self):
        pass


    def tearDown(self):
        pass

    def test_instantiation_unrestricted(self):
        self.assert_(SearchManager(UnrestrictedSearch) is not None)

    def test_instantiation_unrestricted_keywords(self):
        self.assert_(SearchManager(KeywordsSearch) is not None)
