"""
    test_comparator_c1
    ~~~~~~~~~~~

    A set of unit tests over ES-DOC compare api.

    :copyright: (c) 2013 by ES-DOCumentation.

"""

# Module imports.
import unittest

from esdoc_api_test.utils import *
from esdoc_api.lib.pycim.cim_constants import *


# Urls to local / remote esdoc api.
_URLS = {
    'LOCAL' : 'http://127.0.0.1:5000/1/compare/setupData/{0}/{1}',
    'REMOTE' : 'https://api.esdocumentation.org/1/compare/setupData/{0}/{1}'
}

# Url being tested.
_URL = _URLS['LOCAL']

# Project of document being tested.
_PROJECT = 'cmip5'

# DRS key 01 of document being tested.
_COMPARATOR = 'c1'




def _do_test(project=_PROJECT,
             comparator=_COMPARATOR,
             expected_status_code=HTTP_RESPONSE_SUCCESS,
             expected_content=None):
    """Executes unit test by invoking esdoc api and asserting response.

    :param project: Project code.
    :param comparator: Comparator type code.
    :param expected_status_code: Expected http response code.
    :param expected_content: Expected http response content.

    :type project: str
    :type comparator: str
    :type expected_status_code: str
    :type expected_content: str
    
    """
    def get_url():
        return _URL.format(comparator, project)

    # Invoke api.
    test_api_get(get_url(),
                 encoding=None,
                 language=None,
                 schema=None,
                 expected_status_code=expected_status_code,
                 expected_content=expected_content)



class TestCompare_C1(unittest.TestCase):
    """
    A set of unit tests over C1 compare api.

    NOTE : All tests assumes that API db has been populated with cmip5 metadata derived from Metafor cmip5 questionnaire.

    """
    def test_setupdata_positive(self):
        """Compare api postive test.

        """
        _do_test()
        

    def test_setupdata_negative_invalid_project(self):
        """Compare api negative test - project unsupported.

        """
        _do_test(project='xxx', expected_status_code=HTTP_RESPONSE_NOT_ACCEPTABLE)


    def test_setupdata_negative_invalid_comparator(self):
        """Compare api negative test - project unsupported.

        """
        _do_test(comparator='xxx', expected_status_code=HTTP_RESPONSE_NOT_ACCEPTABLE)



