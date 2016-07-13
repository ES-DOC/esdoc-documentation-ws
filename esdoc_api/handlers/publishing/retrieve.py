# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.retrieve.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing retrieve document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import pyesdoc

from esdoc_api import db
from esdoc_api.utils import config
from esdoc_api.utils.http import HTTPRequestHandler



# Query parameter names.
_PARAM_ENCODING = 'encoding'
_PARAM_DOCUMENT_ID = 'id'
_PARAM_DOCUMENT_VERSION = 'version'


# Query parameter validation schema.
_REQUEST_VALIDATION_SCHEMA = {
    _PARAM_DOCUMENT_ID: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_DOCUMENT_VERSION: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_ENCODING: {
        'allowed_case_insensitive': pyesdoc.ENCODINGS_ALL,
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    }
}


class DocumentRetrieveRequestHandler(HTTPRequestHandler):
    """Publishing retrieve document request handler.

    """
    def get(self):
        """HTTP GET handler.

        """
        def _decode_request():
            """Decodes request.

            """
            self.document_id = self.get_argument(_PARAM_DOCUMENT_ID)
            self.document_version = self.get_argument(_PARAM_DOCUMENT_VERSION)
            self.encoding = self.get_argument(_PARAM_ENCODING)


        def _format_params():
            """Formats request parameters.

            """
            self.document_id = self.document_id.lower()
            self.document_version = self.document_version.lower()
            self.encoding = self.encoding.lower()


        def _set_data():
            """Pulls data from db.

            """
            db.session.start(config.db)
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


        self.invoke(_REQUEST_VALIDATION_SCHEMA, [
            _decode_request,
            _format_params,
            _set_data,
            _set_output
            ]
            )
