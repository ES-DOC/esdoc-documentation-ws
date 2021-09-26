# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_id.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search by id request handler.

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
    ('id', lambda v: v.lower()),
    ('version', lambda v: v.lower()),
}


class DocumentByIDSearchRequestHandler(tornado.web.RequestHandler):
    """Document by id search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Headers, "x-requested-with")
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Methods, 'POST, GET, OPTIONS')


    def get(self):
        """HTTP GET handler.

        """
        def _set_data():
            """Pulls data from db.

            """
            db.session.start(config.db)
            self.docs = db.dao.get_document(self.id, self.version, self.project)


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
