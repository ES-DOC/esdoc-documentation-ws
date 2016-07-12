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

from esdoc_api import db
from esdoc_api import utils
from esdoc_api.utils import config



def _get_params():
    """Returns query parameter validation specification."""
    return {
        'encoding': {
            'required': True,
            'whitelist': pyesdoc.ENCODINGS_ALL,
            'value_formatter': lambda v : v.lower()
        },
        'document_id': {
            'required': True,
            'value_formatter': lambda v : v.lower()
        },
        'document_version': {
            'required' : True,
            'value_formatter': lambda v : v.lower()
        }
    }


class DocumentRetrieveRequestHandler(tornado.web.RequestHandler):
    """Publishing retrieve document request handler.

    """
    def prepare(self):
        """Prepare handler state for processing.

        """
        # Start db session.
        db.session.start(config.db)


    def _parse_request_params(self):
        """Parses url query parameters.

        """
        utils.up.parse(self, _get_params())


    def _read_from_archive(self):
        """Loads document from archive.

        """
        self.doc = pyesdoc.archive.read(self.document_id,
                                        self.document_version,
                                        False)


    def _set_response(self):
        """Sets response.

        """
        if self.doc:
            self.output_encoding = self.encoding
            self.output = pyesdoc.encode(self.doc, self.encoding)
        else:
            self.set_status(404)


    def get(self):
        """HTTP GET handler.

        """
        utils.h.invoke(self, (
            self._parse_request_params,
            self._read_from_archive,
            self._set_response
            ))
