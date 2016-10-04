# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_external_id.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search by external id request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api import db
from esdoc_api import utils
from esdoc_api.utils import config
from esdoc_api.utils import constants
from esdoc_api.utils.http import process_request
from esdoc_api.handlers.search.document import set_output
from esdoc_api.handlers.search.document import parse_params



# Query parameters.
_PARAMS = {
    'externalID',
    'externalType'
}

# Maximum number of DRS keys allowed ina path declaration.
_MAX_DRS_KEYS = 8

# Seperator used to delineate DRS keys.
_DRS_SEPERATOR = '/'


class DocumentByExternalIDSearchRequestHandler(tornado.web.RequestHandler):
    """Document by external id search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def get(self):
        """HTTP GET handler.

        """
        def _validate_criteria():
            """Validates url request params.

            """
            # Set search manager.
            self.handler = utils.external_id.get(self.project, self.external_type)
            if not self.handler:
                raise ValueError("External ID type is unsupported.")

            # Validate external id.
            if not self.handler.is_valid(self.external_id):
                raise ValueError("Request parameter externalID: is invalid.")


        def _set_external_id():
            """Sets parsed external identifier.

            """
            self.external_id = self.handler.get_parsed(self.external_id)


        def _set_data():
            """Pulls data from db.

            """
            db.session.start(config.db)
            self.docs = self.handler.do_search(self.project, self.external_id)


        # Process request.
        process_request(self, [
            lambda: parse_params(self, _PARAMS),
            _validate_criteria,
            _set_external_id,
            _set_data,
            lambda: set_output(self, self.docs)
            ])
