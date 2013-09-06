"""
.. module:: esdoc_api.controllers.frontend
   :platform: Unix, Windows
   :synopsis: Encapsulates api front-end operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.lib.controllers import BaseSitePageController

from pylons.templating import render_mako as render



class FrontendController(BaseSitePageController):
    """API front end controller.

    """

    def info(self):
        """Renders standard information page.

        :returns: Information page.
        :rtype: html
        
        """
        return render("/index.html")
