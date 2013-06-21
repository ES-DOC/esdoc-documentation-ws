"""
A set of unit tests utility functions/constants.
"""

# Module imports.
import requests
import sys

from lxml import etree as et

from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_DEFAULT_ENCODING
from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_DEFAULT_LANGUAGE
from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_DEFAULT_SCHEMA
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *



def get_test_file_path(file_name):
    """Returns file path for a test file.

    :param file_name: File name.

    :type file_name: str

    """
    for path in sys.path:
        if path.endswith('esdoc_api_test'):
            return path + '/test_data/{0}'.format(file_name)
    return None


def get_test_xml_file(file_name):
    """Opens & returns a test xml file.

    :param file_name: File name.
    
    :type file_name: str

    """
    return et.parse(get_test_file_path(file_name))


def test_api_get(url,
                 encoding=CIM_DEFAULT_ENCODING,
                 language=CIM_DEFAULT_LANGUAGE,
                 schema=CIM_DEFAULT_SCHEMA,
                 expected_status_code=HTTP_RESPONSE_SUCCESS,
                 expected_content=None):
    """Tests API http GET request.

    :param url: URL to call.
    :param encoding: Document encoding.
    :param language: Document language.
    :param schema: Document schema.
    :param expected_status_code: Expected http response code.
    :param expected_content: Expected http response content.

    :type project: str
    :type url: str
    :type encoding: str
    :type language: str
    :type schema: str
    :type expected_status_code: str
    :type expected_content: str

    """
    # Set payload.
    payload = {}
    if schema is not None:
        payload['schema'] = schema
    if encoding is not None:
        payload['encoding'] = encoding
    if language is not None:
        payload['language'] = language

    # Invoke API.
    response = requests.get(url, params=payload)

    # Assert response.
    assert(response.status_code == expected_status_code)
    if expected_content is not None:
        assert(response._content == expected_content)
        
