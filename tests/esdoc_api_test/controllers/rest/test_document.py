"""A set of unit tests over cim documents RESTful api.

"""
# Module imports.
from esdoc_api.lib.pyesdoc.ontologies.constants import CIM_DEFAULT_SCHEMA
from esdoc_api.lib.utils.http_utils import HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE
from esdoc_api_test.controllers.utils import *
from esdoc_api.lib.pyesdoc.ontologies.constants import *


# Urls to local cim documents RESTful web service.
URL_COLLECTION_LOCAL = 'http://127.0.0.1:5000/1/rest/document/cmip5'
URL_INSTANCE_LOCAL = 'http://127.0.0.1:5000/1/rest/document/cmip5/{0}/{1}'

# Urls to remote cim documents RESTful web service.
URL_COLLECTION_REMOTE = 'https://esdocumentation.org/1/rest/document/cmip5'
URL_INSTANCE_REMOTE = 'https://esdocumentation.org/1/rest/document/cmip5/{0}/{1}'

# Urls being tested.
URL_COLLECTION = URL_COLLECTION_LOCAL
URL_INSTANCE = URL_INSTANCE_LOCAL

# Test cim xml document name.
TEST_FILE_1 = 'cim15.data.data_object.1.xml'
TEST_FILE_1 = 'cim15.data.data_object.2.xml'


class TestDocumentRestAPI(unittest.TestCase):
    """
    A set of unit tests over cim documents RESTful api.
    """
    def setUp(self):
        """Unit test set up (invoked prior to each test execution).

        """
        self.__http = httplib2.Http('.cache')
        self.__api_response = None
        self.__api_content = None

        self.__instance_uid = str(uuid.uuid4())
        self.__instance_lang = CIM_DEFAULT_LANGUAGE
        self.__instance_schema = CIM_DEFAULT_SCHEMA
        self.__instance_url = URL_INSTANCE.format(self.__instance_uid, CIM_DOC_VERSION_LATEST)

        self.__instance_v1_xml = None
        self.__instance_v1_version = 1        
        self.__instance_v1_url = URL_INSTANCE.format(self.__instance_uid, self.__instance_v1_version)

        self.__instance_v2_xml = None
        self.__instance_v2_version = 2
        self.__instance_v2_url = URL_INSTANCE.format(self.__instance_uid, self.__instance_v2_version)
        
        self.__load_cim_xml()


    def __load_cim_xml(self):
        """Loads xml representation of a cim document.

        """
        # V1.
        xml = get_test_xml_file(self.__instance_schema, TEST_FILE_1)
        cim_element(xml, 'documentID').text = self.__instance_uid
        cim_element(xml, 'documentVersion').text = str(self.__instance_v1_version)
        self.__instance_v1_xml = et.tostring(xml)
        
        # V2.
        cim_element(xml, 'documentVersion').text = str(self.__instance_v2_version)
        self.__instance_v2_xml = et.tostring(xml)


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


    def __do_post(self):
        """Posts, i.e. uploads, test cim xml documents.

        """
        def upload(doc_uid, doc_version, doc_xml):
            # Upload document.
            self.__call_api(URL_COLLECTION,
                            verb=HTTP_VERB_POST,
                            headers={
                                HTTP_REQUEST_HEADER_ACCEPT : CIM_MEDIA_TYPE_V15_XML,
                                HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : CIM_DEFAULT_LANGUAGE
                            },
                            payload=doc_xml)
            uid, version, content = self.__deserialize_response()

            # Assert that UID / Version / XML are unchanged.
            assert uid == doc_uid
            assert int(version) == doc_version
            assert content == doc_xml
            
        upload(self.__instance_uid,
               self.__instance_v1_version,
               self.__instance_v1_xml)
        upload(self.__instance_uid,
               self.__instance_v2_version,
               self.__instance_v2_xml)


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
            assert uid == self.__instance_uid
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
            
        retrieve(self.__instance_url, 2)
        retrieve(self.__instance_v1_url, 1)
        retrieve(self.__instance_v2_url, 2)


    def __do_delete(self):
        """Deletes, i.e. retrieves, test cim xml documents via rest api.

        """
        # Invoke api.
        self.__call_api(self.__instance_v1_url,
                        verb=HTTP_VERB_DELETE,
                        headers={
                            HTTP_REQUEST_HEADER_ACCEPT : CIM_MEDIA_TYPE_V15_XML,
                            HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : CIM_DEFAULT_LANGUAGE
                        })
        self.__call_api(self.__instance_v2_url,
                        verb=HTTP_VERB_DELETE,
                        headers={
                            HTTP_REQUEST_HEADER_ACCEPT : CIM_MEDIA_TYPE_V15_XML,
                            HTTP_REQUEST_HEADER_ACCEPT_LANGUAGE : CIM_DEFAULT_LANGUAGE
                        })

        # Verify documents are no longer found.
        self.__retrieve(self.__instance_url,
                        http_response=HTTP_RESPONSE_NOT_FOUND)
        self.__retrieve(self.__instance_v1_url,
                        http_response=HTTP_RESPONSE_NOT_FOUND)
        self.__retrieve(self.__instance_v2_url,
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

        update(self.__instance_v1_url,
               self.__instance_uid,
               self.__instance_v1_version,
               self.__instance_v1_xml)
        update(self.__instance_v2_url,
               self.__instance_uid,
               self.__instance_v2_version,
               self.__instance_v2_xml)


    def test_00(self):
        """Tests that cim xml documents are being loaded into memory correctly.

        """
        assert self.__instance_v1_xml is not None
        assert self.__instance_v2_xml is not None


    def test_01(self):
        """Tests full life cycle of a CIM instance.

        By necessity this creates, retrieves, updates, & deletes a CIM instance in multiple versions.
        """
        # Create instance.
        self.__do_post()
        print 'TEST POST - success'

        # Retrieve instance.
        self.__do_get()
        print 'TEST GET - success'

        # Update instance.
        self.__do_put()
        print 'TEST PUT - success'

        # Delete instance.
        self.__do_delete()
        print 'TEST DELETE - success'


