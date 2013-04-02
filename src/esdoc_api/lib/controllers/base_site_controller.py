from esdoc_api.lib.controllers.base_controller import *


class BaseSiteController(BaseController):
    """
    Base class for all Metafor application controllers.
    """    
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = ABCMeta

    def __init__(self):
        """
        Initialises controller state.
        """
        super(BaseSiteController,self).__init__()
        
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
            cache_data.register('Institute', Institute.get_all())
            cache_data.register('DocumentLanguage', DocumentLanguage.get_all())
            cache_data.register('DocumentSchema', DocumentSchema.get_all())
            cache_data.register('Project', Project.get_all())
            return cache_data

        def load_static_data_level1():
            """
            Append non-static but frequently used data.
            """
            pass
        

        # Load cache data & append to context.
        c.cache = load_cache_data_level0()
        load_static_data_level1()
