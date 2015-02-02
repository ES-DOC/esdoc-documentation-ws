# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.create.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing create document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

import pyesdoc

from esdoc_api import utils



# Supported content types.
_CONTENT_TYPE_JSON = [
    "application/json",
    "application/json; charset=UTF-8"
]


class DocumentCreateRequestHandler(tornado.web.RequestHandler):
    """Publishing create document request handler.

    """
    def _validate_request_headers(self):
        """Validates request headers.

        """
        utils.h.validate_http_content_type(self, _CONTENT_TYPE_JSON)


    def _validate_request_payload(self):
        """Validates request payload.

        """
        # Decode document.
        doc = pyesdoc.decode(self.request.body, 'json')

        # Validate document.
        if not pyesdoc.is_valid(doc):
        	raise utils.h.API_Exception("Document is invalid.")

        # Validate document version.
        if doc.meta.version <= 0:
        	raise utils.h.API_Exception("Document version is invalid.")

        # Validation passed therefore cache decoded payload.
        self.doc = doc


    def _validate_publication_status(self):
    	"""Validates whether document has not already been published.

        """
    	if pyesdoc.archive.exists(self.doc.meta.id, self.doc.meta.version):
        	raise utils.h.API_Exception("Document already published.")


    def _write_to_archive(self):
    	"""Archives document so that it is available for ingestion.

        """
        pyesdoc.archive.write(self.doc)


    def post(self):
        """HTTP POST handler.

        """
        utils.h.invoke(self, (
            self._validate_request_headers,
            self._validate_request_payload,
            self._validate_publication_status,
            self._write_to_archive
            ))

