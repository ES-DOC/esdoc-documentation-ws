# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.create.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing create document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

import pyesdoc

from esdoc_api import db
from esdoc_api import utils
from esdoc_api.utils import config



# Supported content types.
_CONTENT_TYPE_JSON = [
    "application/json",
    "application/json; charset=UTF-8"
]

# HTTP header - Content-Type.
_HTTP_HEADER_CONTENT_TYPE = "Content-Type"



class DocumentCreateRequestHandler(tornado.web.RequestHandler):
    """Publishing create document request handler.

    """
    def _validate_request_headers(self):
        """Validates request headers.

        """
        if _HTTP_HEADER_CONTENT_TYPE not in self.request.headers:
            raise ValueError("Content-Type HTTP header is required")

        header = self.request.headers[_HTTP_HEADER_CONTENT_TYPE]
        if not header in [_CONTENT_TYPE_JSON]:
            raise ValueError("Content-Type is unsupported")

    def _validate_request_payload(self):
        """Validates request payload.

        """
        # Decode document.
        doc = pyesdoc.decode(self.request.body, 'json')
        if not doc:
            raise utils.h.API_Exception("Document could not be decoded.")

        # Minimally validate document.
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
    	"""Archives document.

        """
        pyesdoc.archive.write(self.doc)


    def _write_to_db(self):
        """Uploads document to db.

        """
        db.session.start(config.db)
        try:
            db.ingest.ingest_doc(self.doc)
        finally:
            db.session.end()


    def post(self):
        """HTTP POST handler.

        """
        utils.h.invoke(self, (
            self._validate_request_headers,
            self._validate_request_payload,
            self._validate_publication_status,
            self._write_to_archive,
            self._write_to_db
            ))
