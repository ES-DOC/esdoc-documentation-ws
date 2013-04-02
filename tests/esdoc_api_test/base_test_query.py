"""
    base_test_query
    ~~~~~~~~~~~

    ES-DOC query api unit test base class.

    :copyright: (c) 2013 by ES-DOCumentation.

"""

# Module imports.
import abc
import unittest

from esdoc_api.lib.pycim.cim_constants import CIM_ENCODING_XML
from esdoc_api.lib.pycim.cim_constants import CIM_ENCODING_JSON
from esdoc_api.lib.utils.http_utils import HTTP_RESPONSE_NOT_ACCEPTABLE


class BaseTestQuery(unittest.TestCase):
    """
    A set of unit tests over document by DRS query api.

    NOTE : All tests assumes that API db has been populated with cmip5 metadata derived from Metafor cmip5 questionnaire.

    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = abc.ABCMeta


    def set_test_fn(self, test_fn):
        """Query api postive test - default.

        :param test_fn: Test function to invoke.

        :type test_fn: function

        """
        self.test_fn = test_fn


    def test_positive_default(self):
        """Query api postive test - default.

        """
        self.test_fn()
        

    def test_positive_xml(self):
        """Query api postive test - xml encoding support.

        """
        self.test_fn(encoding=CIM_ENCODING_XML)


    def test_positive_json(self):
        """Query api postive test - json encoding support.

        """
        self.test_fn(encoding=CIM_ENCODING_JSON)


    def test_negative_invalid_schema(self):
        """Query api negative test - schema unsupported.

        """
        self.test_fn(schema='xxx', expected_status_code=HTTP_RESPONSE_NOT_ACCEPTABLE)


    def test_negative_invalid_encoding(self):
        """Query api negative test - encoding unsupported.

        """
        self.test_fn(encoding='xxx', expected_status_code=HTTP_RESPONSE_NOT_ACCEPTABLE)


    def test_negative_invalid_language(self):
        """Query api negative test - language unsupported.

        """
        self.test_fn(language='xxx', expected_status_code=HTTP_RESPONSE_NOT_ACCEPTABLE)


    def test_negative_invalid_project(self):
        """Query api negative test - project unsupported.

        """
        self.test_fn(project='xxx', expected_status_code=HTTP_RESPONSE_NOT_ACCEPTABLE)

