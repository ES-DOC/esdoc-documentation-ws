# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_name.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search by name request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api import db
from esdoc_api.utils import config
from esdoc_api.utils import constants
from esdoc_api.utils.http import process_request
from esdoc_api.handlers.search.document import set_output
from esdoc_api.handlers.search.document import parse_params



# Query parameters.
_PARAMS = {
    'institute',
    'name',
    'type'
    }


class DocumentByNameSearchRequestHandler(tornado.web.RequestHandler):
    """Document by name search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def get(self):
        """HTTP GET handler.

        """
        def _set_data():
            """Pulls data from db.

            """
            db.session.start(config.db)
            self.docs = db.dao.get_document_by_name(self.project,
                                                    self.type,
                                                    self.name,
                                                    self.institute)


        # Process request.
        process_request(self, [
            lambda: parse_params(self, _PARAMS),
            _set_data,
            lambda: set_output(self, self.docs)
            ])


    def options(self, *args):
        """HTTP OPTIONS handler.

        """        
        self.set_status(204)
        self.finish()
