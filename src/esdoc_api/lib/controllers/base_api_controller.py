from esdoc_api.lib.controllers.base_controller import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *


class BaseAPIController(BaseController):
    """
    Base class for all Metafor api controllers.
    """
    def __init__(self):
        """
        Initialises controller state.
        """
        super(BaseAPIController,self).__init__()
        self.__load_cache_data()


    def __call__(self, environ, start_response):
        """
        Invoke the Controller
        """
        self.__set_api_info()
        self.__set_cim_info()
        return super(BaseAPIController,self).__call__(environ, start_response)


    @property
    def controller_type_description(self):
        """
        Gets type controller type description.
        """
        return "WEB SERVICE"


    @abstractproperty
    def validate_doc_request_info(self):
        """
        Gets flag indicating whether http request information should be validated or not.
        """
        pass


    @property
    def is_in_test_mode(self):
        """Gets flag whether api is being invoked in test mode."""
        return self.api_mode == 'test'


    def __set_api_info(self):
        """
        Assign api mode (changes behaviour for testing purposes).
        """
        mode = 'live'

        # Derive from url param (apimode).
        if request.params.has_key('apimode'):
            mode = request.params['apimode']

        self.api_mode = mode


    def __set_cim_info(self):
        """
        Strips various cim information from incoming http request headers.
        """
        # Assign cim info values.        
        self.__set_cim_schema()
        self.__set_cim_encoding()
        self.__set_cim_language()

        # Set flag indicating whether cim info is acceptable for document processing.
        self.is_cim_info_valid = \
           self.cim_encoding is not None and \
           self.cim_language is not None and \
           self.cim_schema is not None


    def __set_cim_encoding(self):
        """
        Derives cim encoding from incoming http request.
        """
        # Assign default.
        encoding_code = CIM_DEFAULT_ENCODING

        # Derive from url param (encoding).
        if request.params.has_key('encoding'):
            encoding_code = request.params['encoding']

        # Map to db entity.
        self.cim_encoding = c.get_cim_encoding(encoding_code)


    def __set_cim_language(self):
        """
        Derives cim language from incoming http request.
        """
        # Assign default.
        language_code = CIM_DEFAULT_LANGUAGE

        # Derive from url param (language).
        if request.params.has_key('language'):
            language_code = request.params['language']

        # Format (if appropriate).
        if isinstance(language_code, str):
            language_code = language_code.split('-')[0].lower()

        # Map to db entity.
        self.cim_language = c.get_cim_language(language_code)
    

    def __set_cim_schema(self):
        """
        Derives cim schema from incoming http request.
        """
        # Assign default.
        schema_code = CIM_DEFAULT_SCHEMA

        # Derive from url param (schema).
        if request.params.has_key('schema'):
            schema_code = request.params['schema']

        # Map to db entity.
        self.cim_schema = c.get_cim_schema(schema_code)
    

    def __load_cache_data(self):
        """
        Loads cache data into processing context.
        """
        @cache_region('static', 'site_cache_data')
        def load():
            """
            Loads static cache data.
            """
            cache_data = CacheData()
            cache_data.register('Institute', Institute.get_all())
            cache_data.register('DocumentEncoding', DocumentEncoding.get_all())
            cache_data.register('DocumentLanguage', DocumentLanguage.get_all())
            cache_data.register('DocumentSchema', DocumentSchema.get_all())
            cache_data.register('Project', Project.get_all())
            return cache_data

        # Load cache data.
        c.cache = load()

        # Set cache helper functions.
        c.get_project = c.cache.get_project
        c.get_institute = c.cache.get_institute
        c.get_cim_encoding = c.cache.get_cim_encoding
        c.get_cim_schema = c.cache.get_cim_schema
        c.get_cim_language = c.cache.get_cim_language


    def get_response_content_type(self):
        """Returns http reponse content type derived from request content type http header.

        """
        if self.cim_encoding in CIM_ENCODINGS:
            return CIM_ENCODINGS[self.cim_encoding]
        else:
            return HTTP_MEDIA_TYPE_JSON

