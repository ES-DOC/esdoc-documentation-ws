"""
    test_query_document_by_id
    ~~~~~~~~~~~

    A set of unit tests over ES-DOC query api.

    :copyright: (c) 2013 by ES-DOCumentation.

"""

# Module imports.
from esdoc_api_test.utils import *
from esdoc_api_test.base_test_query import BaseTestQuery
from esdoc_api.lib.pyesdoc.utils.ontologies import *


# Urls to local / remote esdoc api.
_URLS = {
    'LOCAL' : 'http://127.0.0.1:5000/1/query/name/{0}/{1}/{2}',
    'REMOTE' : 'https://api.esdocumentation.org/1/query/name/{0}/{1}/{2}'
}

# Url being tested.
_URL = _URLS['LOCAL']

# Project of document being tested.
_PROJECT = 'cmip5'

# Type of document being tested.
_TYPE = 'SIMULATIONRUN'

# Name of document being tested.
_NAME = 'DECADAL1960-MR'



def _do_test(project=_PROJECT,
             type=_TYPE,
             name=_NAME,
             encoding=CIM_DEFAULT_ENCODING,
             language=CIM_DEFAULT_LANGUAGE,
             schema=CIM_DEFAULT_SCHEMA,
             expected_status_code=HTTP_RESPONSE_SUCCESS,
             expected_content=None):
    """Executes unit test by invoking esdoc api and asserting response.

    :param project: Document project code.
    :param type: Document type.
    :param name: Document name.
    :param encoding: Document encoding.
    :param language: Document language.
    :param schema: Document schema.
    :param expected_status_code: Expected http response code.
    :param expected_content: Expected http response content.

    :type project: str
    :type type: str
    :type name: str
    :type encoding: str
    :type language: str
    :type schema: str
    :type expected_status_code: str
    :type expected_content: str
    
    """
    def get_url():
        return _URL.format(project, type, name)

    # Invoke api.
    test_api_get(get_url(), encoding, language, schema, expected_status_code, expected_content)



class TestQuery_DocumentByName(BaseTestQuery):
    """
    A set of unit tests over document by name query api.

    NOTE : All tests assumes that API db has been populated with cmip5 metadata derived from Metafor cmip5 questionnaire.

    """
    def setUp(self):
        """Test case set up.

        """
        super(TestQuery_DocumentByName, self).set_test_fn(_do_test)


    def test_negative_no_data_01(self):
        """Query api negative test - no data.

        """
        _do_test(type='xxx', expected_content='[]')


    def test_negative_no_data_02(self):
        """Query api negative test - no data.

        """
        _do_test(name='xxx', expected_content='[]')

