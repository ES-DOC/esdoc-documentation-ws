# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.retrieve.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing retrieve document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

import pyesdoc

from esdoc_api.utils.http import process_request



# Query parameter names.
_PARAM_DOCUMENT_ID = 'document_id'
_PARAM_DOCUMENT_VERSION = 'document_version'
_PARAM_ENCODING = 'encoding'



class DocumentRetrieveRequestHandler(tornado.web.RequestHandler):
    """Publishing retrieve document request handler.

    """
    def get(self):
        """HTTP GET handler.

        """
        def _set_criteria():
            """Sets search criteria.

            """
            for param in {
                _PARAM_DOCUMENT_ID,
                _PARAM_DOCUMENT_VERSION,
                _PARAM_ENCODING
            }:
                setattr(self, param, self.get_argument(param).lower())


        def _set_data():
            """Pulls data from db.

            """
            self.doc = pyesdoc.archive.read(self.document_id,
                                            self.document_version,
                                            False)


        def _set_output():
            """Sets output data to be returned to client.

            """
            if self.doc is None:
                self.set_status(404)
            else:
                self.output_encoding = self.encoding
                self.output = pyesdoc.encode(self.doc, self.encoding)


        # Process request.
        process_request(self, [
            _set_criteria,
            _set_data,
            _set_output
            ])
