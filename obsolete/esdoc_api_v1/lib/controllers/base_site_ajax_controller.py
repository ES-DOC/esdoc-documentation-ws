# -*- coding: utf-8 -*-

from esdoc_api.lib.controllers.base_controller import *


class BaseSiteAjaxController(BaseController):
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

