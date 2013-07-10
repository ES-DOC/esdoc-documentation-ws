from esdoc_api.lib.controllers.base_site_controller import *
from esdoc_api.lib.utils.site_factory import create_site_map


class BaseSitePageController(BaseSiteController):
    """Base front end page controller.
    
    """

    def __init__(self):
        """
        Initialises controller state.
        """
        super(BaseSitePageController,self).__init__()

        # Set common context info.
        c.site = create_site_map(role='public', path=request.path)
        c.section = c.site.page.parent
        c.page = c.site.page


    @property
    def controller_type_description(self):
        """
        Gets type controller type description.
        """
        return "SITE PAGE"
