"""
.. module:: esdoc_api.controllers.frontend
   :platform: Unix, Windows
   :synopsis: Encapsulates api front-end operations.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.lib.controllers import *
import esdoc_api.lib.repo.dao as dao


class FrontendController(BaseSitePageController):
    """API front end controller.

    """

    def info(self):
        """Renders standard information page.

        :returns: Information page.
        :rtype: html
        
        """
        return render("/pages/site-about.xhtml")


    def ingest_history(self):
        """Renders ingestion history page.

        :returns: Ingestion history page.
        :rtype: html

        """
        # Set context and render.
        c.ingest_history = dao.get_all(IngestHistory)
        return render("/pages/site-ingestion-history.xhtml")
    