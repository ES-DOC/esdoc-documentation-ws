"""A set of unit tests over cim documents RESTful api.

"""
# Module imports.
import requests
import unittest

from esdoc_api.lib.pyesdoc.utils.ontologies import CIM_DEFAULT_SCHEMA
from esdoc_api.lib.utils.http_utils import HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE
from esdoc_api_test.utils import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *


# Urls to local / remote esdoc api.
_URLS = {
    'LOCAL' : 'http://127.0.0.1:5000/1/publish/{0}',
    'REMOTE' : 'https://api.esdocumentation.org/1/publish/{0}'
}

# Urls being tested.
_URL = _URLS['LOCAL']
_URL_INSTANCE = _URL + '/{1}/{2}'

# Project of document being tested.
_PROJECT = 'cmip5'

# Test document template.
_TEMPLATE = 'cim15.data.data_object.1.xml'

# Test document unique identifier.
_UID = 'e9ebb2d9-f6dc-4d29-a1e1-ae132444b453'



class DocumentInfo(object):
    """Encapsulate information pertaining to a document.

    """
    def __init__(self, uid, version):
        """Ctor.

        :param uid: Document unique identifier.
        :param version: Document version.

        :type uid: str
        :type version: str

        """
        def set_content():
            template = get_test_xml_file(_TEMPLATE)
            cim_element(template, 'documentID').text = uid
            cim_element(template, 'documentVersion').text = str(version)
            self.content = et.tostring(template)
            self.content_xml = et.fromstring(self.content)

        self.project = _PROJECT
        self.uid = uid
        self.version = version
        self.url = _URL_INSTANCE.format(_PROJECT, uid, version)
        self.url_collection = _URL.format(_PROJECT)
        self.language = CIM_DEFAULT_LANGUAGE
        self.schema = CIM_DEFAULT_SCHEMA

        set_content()

    @classmethod
    def do_assert(cls,
                  document,
                  uid,
                  version,
                  project=_PROJECT,
                  language=CIM_DEFAULT_LANGUAGE,
                  schema=CIM_DEFAULT_SCHEMA):
        """Performs a set of asserts in order to ensure that document is consistent.

        :param document: Document information.
        :param uid: Document unique identifier.
        :param version: Document version.

        :type document: DocumentInfo
        :type uid: str
        :type version: str

        """
        assert document is not None
        assert isinstance(document, DocumentInfo)
        assert document.uid == uid
        assert document.uid == cim_element(document.content_xml, 'documentID').text
        assert document.version == version
        assert document.version == cim_element(document.content_xml, 'documentVersion').text
        assert document.project == project
        assert document.language == language
        assert document.schema == schema
        assert document.url == _URL_INSTANCE.format(project, uid, version)
        assert document.url_collection == _URL.format(project)
        


class TestDocumentRestAPI(unittest.TestCase):
    """
    A set of unit tests over cim documents RESTful api.
    """
    def setUp(self):
        """Unit test set up (invoked prior to each test execution).

        """
        self.document_v1 = DocumentInfo(_UID, '1')
        self.document_v2 = DocumentInfo(_UID, '2')
        self.documents = [self.document_v1, self.document_v2]


    def __call_api(self,
                   url,
                   verb,
                   headers= {},
                   payload=None,
                   http_response=HTTP_RESPONSE_SUCCESS):
        """Invokes web service api.
        
        Keyword Arguments:

        url - url to test.
        verb - http request verb to apply.
        headers - http request headers to apply.
        payload - http request payload.
        http_response - expected http response.

        """
        # Invoke endpoint.
        if payload is None:
            self.__api_response, self.__api_content = \
                self.__http.request(url, verb, headers=headers)
        else:
            self.__api_response, self.__api_content = \
                self.__http.request(url, verb, headers=headers, body=payload)

        # Do standard asserts.
        assert(self.__api_response is not None)
        print url, verb, self.__api_response.status, http_response, headers
        assert(self.__api_response.status == http_response)


    def __deserialize_response(self):
        """Deserializes web service api response.

        """
        # XML;
        xml = self.__api_content.decode(CIM_UNICODE)
        assert xml is not None
        xml = et.fromstring(xml)

        # UID;
        uid = cim_element(xml, 'documentID')
        assert uid is not None
        uid = uid.text
        
        # Version;
        version = cim_element(xml, 'documentVersion')
        assert version is not None
        version = version.text

        return uid, version, et.tostring(xml)


    def do_post(self):
        """Posts, i.e. uploads, test cim xml documents.

        """
        def post(document):
            print document.url_collection
            r = requests.post(document.url_collection, data=document.content)
            print r

#            payload = dict()
#            # Upload document.
#            self.__call_api(URL_COLLECTION,
#                            verb=HTTP_VERB_POST,
#                            headers={
#                                HTTP_REQUEST_HEADER_ACCEPT : CIM_MEDIA_TYPE_V15_XML,
#                                HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : CIM_DEFAULT_LANGUAGE
#                            },
#                            payload=document.content)
#            uid, version, content = self.__deserialize_response()
#
#            # Assert that UID / Version / Content are unchanged.
#            assert uid == document.uid
#            assert version == document.version
#            assert content == document.content

        for document in self.documents:
            post(document)


    def __retrieve(self,
                   url,
                   encoding=CIM_DEFAULT_ENCODING,
                   language=CIM_DEFAULT_LANGUAGE,
                   schema=CIM_DEFAULT_SCHEMA,
                   http_response=HTTP_RESPONSE_SUCCESS,
                   deserialize=False,
                   expected_version=1):
        """Retrieves remote cim xml document via rest api.

        Keyword Arguments:

        url - url to test.
        http_response - expected http response.
        deserialize - flag instructing whether to deserialize response or not.
        expected_version - expected document version.

        """
        # Derive media type.
        media_type = get_cim_media_type(schema, encoding)

        # Call api.
        self.__call_api(url,
                        verb=HTTP_VERB_GET,
                        headers={
                            HTTP_REQUEST_HEADER_ACCEPT : media_type,
                            HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : language
                        },
                        http_response=http_response)

        if deserialize & self.__api_response.status == HTTP_RESPONSE_SUCCESS:
            uid, version, xml = self.__deserialize_response()
            assert uid == self.document_uid
            assert version == expected_version
            

    def __do_get(self):
        """Gets, i.e. retrieves, test cim xml documents via rest api.

        """
        def retrieve(url, expected_version):
            # ... positive tests.
            self.__retrieve(url)
            self.__retrieve(url, encoding=CIM_ENCODING_XML,
                            deserialize=True, expected_version=expected_version)
            self.__retrieve(url, encoding=CIM_ENCODING_JSON)

            # ... negative tests.
            self.__retrieve(url, language='xxx',
                            http_response=HTTP_RESPONSE_NOT_ACCEPTABLE)
            self.__retrieve(url, encoding='xxx',
                            http_response=HTTP_RESPONSE_NOT_ACCEPTABLE)
            self.__retrieve(url, schema='xxx',
                            http_response=HTTP_RESPONSE_NOT_ACCEPTABLE)
            self.__retrieve(url.replace('cmip5', 'xxx'),
                            http_response=HTTP_RESPONSE_NOT_ACCEPTABLE)
            
        retrieve(self.document_url, 2)
        retrieve(self.document_v1_url, 1)
        retrieve(self.document_v2_url, 2)


    def __do_delete(self):
        """Deletes, i.e. retrieves, test cim xml documents via rest api.

        """
        # Invoke api.
        self.__call_api(self.document_v1_url,
                        verb=HTTP_VERB_DELETE,
                        headers={
                            HTTP_REQUEST_HEADER_ACCEPT : CIM_MEDIA_TYPE_V15_XML,
                            HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : CIM_DEFAULT_LANGUAGE
                        })
        self.__call_api(self.document_v2_url,
                        verb=HTTP_VERB_DELETE,
                        headers={
                            HTTP_REQUEST_HEADER_ACCEPT : CIM_MEDIA_TYPE_V15_XML,
                            HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : CIM_DEFAULT_LANGUAGE
                        })

        # Verify documents are no longer found.
        self.__retrieve(self.document_url,
                        http_response=HTTP_RESPONSE_NOT_FOUND)
        self.__retrieve(self.document_v1_url,
                        http_response=HTTP_RESPONSE_NOT_FOUND)
        self.__retrieve(self.document_v2_url,
                        http_response=HTTP_RESPONSE_NOT_FOUND)


    def __do_put(self):
        """Puts, i.e. updates, test cim xml documents via rest api.

        """
        def update(doc_url, doc_uid, doc_version, doc_xml):
            # Upload document.
            self.__call_api(doc_url,
                            verb=HTTP_VERB_PUT,
                            headers={
                                HTTP_REQUEST_HEADER_ACCEPT : CIM_MEDIA_TYPE_V15_XML,
                                HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : CIM_DEFAULT_LANGUAGE
                            },
                            payload=doc_xml)

            # Assert that UID / Version / XML are unchanged.
            uid, version, content = self.__deserialize_response()
            assert uid == doc_uid
            assert int(version) == doc_version
            assert content == doc_xml

        update(self.document_v1_url,
               self.document_uid,
               self.document_v1_version,
               self.document_v1_xml)
        update(self.document_v2_url,
               self.document_uid,
               self.document_v2_version,
               self.document_v2_xml)


    def test_setup_v1(self):
        """Tests that document v1 has been setup correctly.

        """
        DocumentInfo.do_assert(self.document_v1, _UID, '1')
        

    def test_setup_v2(self):
        """Tests that document v2 has been setup correctly.

        """
        DocumentInfo.do_assert(self.document_v2, _UID, '2')



    def test_01(self):
        """Tests full life cycle of a CIM instance.

        By necessity this creates, retrieves, updates, & deletes a CIM instance in multiple versions.
        """
        # Create instance.
        self.do_post()
        print 'TEST POST - success'

#        # Retrieve instance.
#        self.__do_get()
#        print 'TEST GET - success'
#
#        # Update instance.
#        self.__do_put()
#        print 'TEST PUT - success'
#
#        # Delete instance.
#        self.__do_delete()
#        print 'TEST DELETE - success'


