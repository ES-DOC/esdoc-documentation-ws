# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document_by_drs.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search by DRS request handler.

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
    ('drsPath', lambda v: v.upper())
}

# Maximum number of DRS keys allowed ina path declaration.
_MAX_DRS_KEYS = 8

# Seperator used to delineate DRS keys.
_DRS_SEPERATOR = '/'


class DocumentByDRSSearchRequestHandler(tornado.web.RequestHandler):
    """Document by DRS search request handler.

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
            if len(self.drs_path.split(_DRS_SEPERATOR)) == 1:
                raise ValueError("A DRS path must contain at least one element")
            if len(self.drs_path.split(_DRS_SEPERATOR)) > _MAX_DRS_KEYS:
                msg = "A DRS path must consist of a maximum {0} keys"
                raise ValueError(msg.format(_MAX_DRS_KEYS))


        def _set_drs_keys():
            """Sets the DRS keys to be used to search db.

            """
            self.drs_keys = [i for i in self.drs_path.split(_DRS_SEPERATOR)
                             if len(i) and i.upper() != self.project.upper()]


        def _set_data():
            """Pulls data from db.

            """
            db.session.start(config.db)
            self.docs = db.dao.get_document_by_drs_keys(
              self.project,
              self.drs_keys[0] if len(self.drs_keys) > 0 else None,
              self.drs_keys[1] if len(self.drs_keys) > 1 else None,
              self.drs_keys[2] if len(self.drs_keys) > 2 else None,
              self.drs_keys[3] if len(self.drs_keys) > 3 else None,
              self.drs_keys[4] if len(self.drs_keys) > 4 else None,
              self.drs_keys[5] if len(self.drs_keys) > 5 else None,
              self.drs_keys[6] if len(self.drs_keys) > 6 else None,
              self.drs_keys[7] if len(self.drs_keys) > 7 else None
              )


        # Process request.
        process_request(self, [
            lambda: parse_params(self, _PARAMS),
            _validate_criteria,
            _set_drs_keys,
            _set_data,
            lambda: set_output(self, self.docs)
            ])



