# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.create.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing create document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import pyesdoc

from esdoc_api import db
from esdoc_api.utils import config
from esdoc_api.utils import exceptions
from esdoc_api.utils.http import HTTPRequestHandler



# Supported content types.
_CONTENT_TYPE_JSON = [
    "application/json",
    "application/json; charset=UTF-8"
]

# HTTP header - Content-Type.
_HTTP_HEADER_CONTENT_TYPE = "Content-Type"



class DocumentCreateRequestHandler(HTTPRequestHandler):
    """Publishing create document request handler.

    """
    def post(self):
        """HTTP POST handler.

        """
        def _validate_request_headers():
            """Validates request headers.

            """
            if _HTTP_HEADER_CONTENT_TYPE not in self.request.headers:
                raise ValueError("Content-Type HTTP header is required")

            header = self.request.headers[_HTTP_HEADER_CONTENT_TYPE]
            if not header in _CONTENT_TYPE_JSON:
                raise ValueError("Content-Type is unsupported")


        def _validate_request_payload():
            """Validates request payload.

            """
            # Decode document.
            doc = pyesdoc.decode(self.request.body, 'json')
            if not doc:
                raise exceptions.API_Exception("Document could not be decoded.")

            # Minimally validate document.
            if not pyesdoc.is_valid(doc):
                raise exceptions.API_Exception("Document is invalid.")

            # Validate document version.
            if doc.meta.version <= 0:
                raise exceptions.API_Exception("Document version is invalid.")

            # Validation passed therefore cache decoded & extended payload.
            self.doc = pyesdoc.extend(doc)


        def _validate_publication_status():
            """Validates whether document has not already been published.

            """
            if pyesdoc.archive.exists(self.doc.meta.id, self.doc.meta.version):
                raise exceptions.API_Exception("Document already published.")


        def _ingest():
            """Ingest document.

            """
            db.session.start(config.db)
            try:
                db.ingest.execute(self.doc)
            finally:
                db.session.end()


        self.invoke(None, [
            _validate_request_headers,
            _validate_request_payload,
            _validate_publication_status,
            _ingest
            ]
            )

