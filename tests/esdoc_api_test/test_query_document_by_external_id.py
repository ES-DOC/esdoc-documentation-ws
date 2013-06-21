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
    'LOCAL' : 'http://127.0.0.1:5000/1/query/externalID/{0}/{1}/{2}',
    'REMOTE' : 'https://api.esdocumentation.org/1/query/externalID/{0}/{1}/{2}'
}

# Url being tested.
_URL = _URLS['LOCAL']

# Project of document being tested.
_PROJECT = 'cmip5'

# Dataset external id type and test value.
DATASET = 'dataset'
DATASET_ID ='cmip5.output1.MOHC.HadGEM2-A.sstClim4xCO2.day.atmos.cfDay.r1i1p1.v20111026'

# File external id type and test value.
FILE = 'file'
FILE_ID ='cmip5.output1.MOHC.HadGEM2-A.sstClim4xCO2.day.atmos.cfDay.r1i1p1.v20111026'


def _do_test(project=_PROJECT,
             external_id_type=DATASET,
             external_id=DATASET_ID,
             encoding=CIM_DEFAULT_ENCODING,
             language=CIM_DEFAULT_LANGUAGE,
             schema=CIM_DEFAULT_SCHEMA,
             expected_status_code=HTTP_RESPONSE_SUCCESS,
             expected_content=None):
    """Executes unit test by invoking esdoc api and asserting response.

    :param project: Document project code.
    :param external_id_type: External ID type.
    :param external_id: External ID.
    :param encoding: Document encoding.
    :param language: Document language.
    :param schema: Document schema.
    :param expected_status_code: Expected http response code.
    :param expected_content: Expected http response content.

    :type project: str
    :type external_id_type: str
    :type external_id: str
    :type encoding: str
    :type language: str
    :type schema: str
    :type expected_status_code: str
    :type expected_content: str

    """
    def get_url():
        return _URL.format(project, external_id_type, external_id)

    # Invoke api.
    test_api_get(get_url(), encoding, language, schema, expected_status_code, expected_content)




class TestQuery_DocumentByExternalID(BaseTestQuery):
    """
    A set of unit tests over document set by external id query api.
    """
    def setUp(self):
        """Test case set up.

        """
        super(TestQuery_DocumentByExternalID, self).set_test_fn(_do_test)


    def test_positive_default_for_file(self):
        """Query api postive test - default.

        """
        _do_test(external_id_type=FILE, external_id=FILE_ID)


    def test_positive_xml_for_file(self):
        """Query api postive test - xml encoding support.

        """
        _do_test(encoding=CIM_ENCODING_XML, external_id_type=FILE, external_id=FILE_ID)


    def test_positive_json_for_file(self):
        """Query api postive test - json encoding support.

        """
        _do_test(encoding=CIM_ENCODING_JSON)


    def test_negative_no_data_01(self):
        """Query api negative test - no data.

        """
        _do_test(external_id_type='xxx', expected_content='[]')


    def test_negative_no_data_02(self):
        """Query api negative test - no data.

        """
        _do_test(external_id='xxx', expected_content='[]')




