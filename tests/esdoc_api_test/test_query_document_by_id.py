"""
    test_query_document_by_id
    ~~~~~~~~~~~

    A set of unit tests over ES-DOC query api.

    :copyright: (c) 2013 by ES-DOCumentation.

"""

# Module imports.
from esdoc_api_test.utils import *
from esdoc_api_test.base_test_query import BaseTestQuery
from esdoc_api.lib.pyesdoc.ontologies.constants import *


# Urls to local / remote esdoc api.
_URLS = {
    'LOCAL' : 'http://127.0.0.1:5000/1/query/id/{0}/{1}/{2}',
    'REMOTE' : 'https://api.esdocumentation.org/1/query/id/{0}/{1}/{2}'
}

# Url being tested.
_URL = _URLS['LOCAL']

# Project of document being tested.
_PROJECT = 'cmip5'

# ID of document being tested.
_ID = '847b34d0-9cc7-11e0-9e0c-00163e9152a5'

# Version of document being tested.
_VERSION = 3



def _do_test(project=_PROJECT,
             id=_ID,
             version=_VERSION,
             encoding=CIM_DEFAULT_ENCODING,
             language=CIM_DEFAULT_LANGUAGE,
             schema=CIM_DEFAULT_SCHEMA,
             expected_status_code=HTTP_RESPONSE_SUCCESS,
             expected_content=None):
    """Executes unit test by invoking esdoc api and asserting response.

    :param project: Document project code.
    :param id: Document ID.
    :param version: Document version.
    :param encoding: Document encoding.
    :param language: Document language.
    :param schema: Document schema.
    :param expected_status_code: Expected http response code.
    :param expected_content: Expected http response content.

    :type project: str
    :type id: str
    :type version: str
    :type encoding: str
    :type language: str
    :type schema: str
    :type expected_status_code: str
    :type expected_content: str
    
    """
    def get_url():
        return _URL.format(project, id, version)

    # Invoke api.
    test_api_get(get_url(), encoding, language, schema, expected_status_code, expected_content)



class TestQuery_DocumentByID(BaseTestQuery):
    """
    A set of unit tests over document by id query api.

    NOTE : All tests assumes that API db has been populated with cmip5 metadata derived from Metafor cmip5 questionnaire.

    """
    def setUp(self):
        """Test case set up.

        """
        super(TestQuery_DocumentByID, self).set_test_fn(_do_test)


    def test_negative_no_data_01(self):
        """Query api negative test - no data.

        """
        _do_test(id='xxx', expected_content='[]')


    def test_negative_no_data_02(self):
        """Query api negative test - no data.

        """
        _do_test(version=999, expected_content='[]')

