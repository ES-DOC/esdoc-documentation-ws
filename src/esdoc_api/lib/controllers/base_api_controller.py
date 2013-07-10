from esdoc_api.lib.controllers.base_controller import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.pyesdoc.utils.ontologies import *
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.cache as cache


class BaseAPIController(BaseController):
    """Base class for all ES-DOC API controllers.

    """
    def __before__(self, action, **kwargs):
        """Pre action invocation handler.

        """
        super(BaseAPIController,self).__before__(action, **kwargs)

        # Set common context info.
        cache.load()
        self.__load_cache_data()
        self.__set_api_info()
        self.__set_doc_metainfo()


    @property
    def controller_type_description(self):
        """Gets type controller type description.
        
        """
        return "WEB SERVICE"


    @property
    def is_in_test_mode(self):
        """Gets flag indicating whether api is being invoked in test mode.

        """
        return self.api_mode == 'test'


    def __set_api_info(self):
        """Assigns api mode (changes behaviour for testing purposes).
        
        """
        mode = 'live'

        # Derive from url param (apimode).
        if request.params.has_key('apimode'):
            mode = request.params['apimode']

        self.api_mode = mode


    def __set_doc_metainfo(self):
        """Assigns document meta-information from incoming http request.
        
        """
        # Assign values.
        setters = [
            self.__set_doc_project,
            self.__set_doc_institute,
            self.__set_doc_ontology,
            self.__set_doc_encoding,
            self.__set_doc_language
        ]
        for setter in setters:
            setter()
            
        # Set flag indicating whether document metainfo is acceptable for document processing.
        self.is_doc_metainfo_valid = self.project is not None and \
                                     self.encoding is not None and \
                                     self.language is not None and \
                                     self.ontology is not None


    def __set_doc_project(self):
        """Assigns document project from incoming http request.

        """        
        self.project = None if not request.params.has_key('project') else \
                       c.get_project(request.params['project'])
        self.project_id = None if self.project is None else self.project.ID


    def __set_doc_institute(self):
        """Assigns document institute from incoming http request.

        """
        self.institute = None if not request.params.has_key('institute') else \
                         c.get_institute(request.params['institute'])
        self.institute_id = None if self.institute is None else self.institute.ID


    def __set_doc_encoding(self):
        """Assigns document encoding from incoming http request.

        """
        self.encoding = None if not request.params.has_key('encoding') else \
                        c.get_encoding(request.params['encoding'])
        self.encoding_id = None if self.encoding is None else self.encoding.ID


    def __set_doc_language(self):
        """Assigns document language from incoming http request.

        """
        self.language = None if not request.params.has_key('language') else \
                        c.get_language(request.params['language'].split('-')[0].lower())
        self.language_id = None if self.language is None else self.language.ID

    

    def __set_doc_ontology(self):
        """Assigns document ontology from incoming http request.

        """
        if request.params.has_key('ontologyName') and \
           request.params.has_key('ontologyVersion'):
            self.ontology = c.get_ontology(request.params['ontologyName'],
                                           request.params['ontologyVersion'])
        else:
            self.ontology = None
        self.ontology_id = None if self.ontology is None else self.ontology.ID


    
    def __load_cache_data(self):
        """Loads cache data into processing context.
        
        """
        @cache_region('static', 'site_cache_data')
        def load():
            """
            Loads static cache data.
            """
            cache_data = CacheData()            
            cache_data.register('Institute', dao.get_all(Institute))
            cache_data.register('DocumentEncoding', dao.get_all(DocumentEncoding))
            cache_data.register('DocumentLanguage', dao.get_all(DocumentLanguage))
            cache_data.register('DocumentOntology', dao.get_all(DocumentOntology))
            cache_data.register('Project', dao.get_all(Project))
            return cache_data

        # Load cache data.
        c.cache = load()

        # Set cache helper functions.
        c.get_project = c.cache.get_project
        c.get_institute = c.cache.get_institute
        c.get_encoding = c.cache.get_encoding
        c.get_ontology = c.cache.get_ontology
        c.get_language = c.cache.get_language

        print 'ZZZ', c.get_language


    def get_response_content_type(self):
        """Returns http reponse content type derived from request content type http header.

        """
        if self.encoding in ESDOC_ENCODINGS:
            return ESDOC_ENCODINGS[self.encoding]
        else:
            return HTTP_MEDIA_TYPE_JSON

