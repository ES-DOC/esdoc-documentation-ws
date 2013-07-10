from esdoc_api.lib.controllers.base_site_controller import *


class BaseSiteAjaxController(BaseSiteController):
    """Base ajax controller.

    """

    def __init__(self):
        """
        Initialises controller state.
        """
        super(BaseSiteAjaxController,self).__init__()

    
    @property
    def controller_type_description(self):
        """
        Gets type controller type description.
        """
        return "SITE AJAX"

