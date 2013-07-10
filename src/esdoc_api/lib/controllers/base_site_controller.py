from esdoc_api.lib.controllers.base_controller import *
import esdoc_api.lib.repo.dao as dao


class BaseSiteController(BaseController):
    """Base front end controller.

    """    
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta
    
        
    def __before__(self, action, **kwargs):
        """Pre action invocation handler.

        """
        super(BaseSiteController,self).__before__(action, **kwargs)

        # Set common context info.
        self.__set_cache_state()


    def __set_cache_state(self):
        """
        Loads cache data into processing context.
        """
        @cache_region('static', 'site_cache_data')
        def load_cache_data_level0():
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

        # Load cache data & append to context.
        c.cache = load_cache_data_level0()

