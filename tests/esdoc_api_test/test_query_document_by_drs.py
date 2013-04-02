"""
    test_query_document_by_id
    ~~~~~~~~~~~

    A set of unit tests over ES-DOC query api.

    :copyright: (c) 2013 by ES-DOCumentation.

"""

# Module imports.
from esdoc_api_test.utils import *
from esdoc_api_test.base_test_query import BaseTestQuery
from esdoc_api.lib.pycim.cim_constants import *


# Urls to local / remote esdoc api.
_URLS = {
    'LOCAL' : 'http://127.0.0.1:5000/1/query/drs/{0}',
    'REMOTE' : 'https://api.esdocumentation.org/1/query/drs/{0}'
}

# Url being tested.
_URL = _URLS['LOCAL']

# Project of document being tested.
_PROJECT = 'cmip5'

# DRS key 01 of document being tested.
_DRS_KEY_01 = 'MPI-M'

# DRS key 02 of document being tested.
_DRS_KEY_02 = 'MPI-ESM-MR'

# DRS key 03 of document being tested.
_DRS_KEY_03 = 'DECADAL1960'

# DRS key 04 of document being tested.
_DRS_KEY_04 = 'R1I1P1'

# DRS key 05 of document being tested.
_DRS_KEY_05 = '1960'

# DRS key 06 of document being tested.
_DRS_KEY_06 = ''

# DRS key 07 of document being tested.
_DRS_KEY_07 = ''

# DRS key 08 of document being tested.
_DRS_KEY_08 = ''



def _do_test(project=_PROJECT,
             drs_key_01=_DRS_KEY_01,
             drs_key_02=_DRS_KEY_02,
             drs_key_03=_DRS_KEY_03,
             drs_key_04=_DRS_KEY_04,
             drs_key_05=_DRS_KEY_05,
             drs_key_06=_DRS_KEY_06,
             drs_key_07=_DRS_KEY_07,
             drs_key_08=_DRS_KEY_08,
             encoding=CIM_DEFAULT_ENCODING,
             language=CIM_DEFAULT_LANGUAGE,
             schema=CIM_DEFAULT_SCHEMA,
             expected_status_code=HTTP_RESPONSE_SUCCESS,
             expected_content=None):
    """Executes unit test by invoking esdoc api and asserting response.

    :param project: Document project code.
    :param drs_key_01: Document DRS key 01.
    :param drs_key_02: Document DRS key 02.
    :param drs_key_03: Document DRS key 03.
    :param drs_key_04: Document DRS key 04.
    :param drs_key_05: Document DRS key 05.
    :param drs_key_06: Document DRS key 06.
    :param drs_key_07: Document DRS key 07.
    :param drs_key_08: Document DRS key 08.
    :param encoding: Document encoding.
    :param language: Document language.
    :param schema: Document schema.
    :param expected_status_code: Expected http response code.
    :param expected_content: Expected http response content.

    :type project: str
    :type drs_key_01: str
    :type drs_key_02: str
    :type drs_key_03: str
    :type drs_key_04: str
    :type drs_key_05: str
    :type drs_key_06: str
    :type drs_key_07: str
    :type drs_key_08: str
    :type encoding: str
    :type language: str
    :type schema: str
    :type expected_status_code: str
    :type expected_content: str
    
    """
    def get_url():
        url = _URL.format(project)
        drs_keys = [
            drs_key_01,
            drs_key_02,
            drs_key_03,
            drs_key_04,
            drs_key_05,
            drs_key_06,
            drs_key_07,
            drs_key_08
        ]
        for drs_key in drs_keys:
            if drs_key is not None and len(drs_key) > 0:
                url += '/'
                url += drs_key
        return url

    # Invoke api.
    test_api_get(get_url(), encoding, language, schema, expected_status_code, expected_content)



class TestQuery_DocumentByDRS(BaseTestQuery):
    """
    A set of unit tests over document by DRS query api.

    NOTE : All tests assumes that API db has been populated with cmip5 metadata derived from Metafor cmip5 questionnaire.

    """
    def setUp(self):
        """Test case set up.

        """
        super(TestQuery_DocumentByDRS, self).set_test_fn(_do_test)
    

    def test_negative_no_data_01(self):
        """Query api negative test - no data.

        """
        _do_test(drs_key_01='xxx', expected_content='[]')


    def test_negative_no_data_02(self):
        """Query api negative test - no data.

        """
        _do_test(drs_key_02='xxx', expected_content='[]')

