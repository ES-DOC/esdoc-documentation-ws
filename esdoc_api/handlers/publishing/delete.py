# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.delete.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing delete document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import pyesdoc

from esdoc_api import db
from esdoc_api.utils import config
from esdoc_api.utils.http import HTTPRequestHandler



# Query parameter names.
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
    }
}


class DocumentDeleteRequestHandler(HTTPRequestHandler):
    """Publishing delete document request handler.

    """
    def delete(self):
        """HTTP DELETE handler.

        """
        def _decode_request():
            """Decodes request.

            """
            self.document_id = self.get_argument(_PARAM_DOCUMENT_ID)
            self.document_version = self.get_argument(_PARAM_DOCUMENT_VERSION)


        def _format_params():
            """Formats request parameters.

            """
            self.document_id = self.document_id.lower()
            self.document_version = self.document_version.lower()


        def _delete_from_archive():
            """Deletes document from archive.

            """
            pyesdoc.archive.delete(self.document_id,
                                   self.document_version)


        def _delete_from_db(self):
            """Deletes document from database.

            """
            db.session.start(config.db)
            try:
                db.ingest.undo(self.document_id, self.document_version)
                db.session.commit()
            finally:
                db.session.end()


        self.invoke(_REQUEST_VALIDATION_SCHEMA, [
            _decode_request,
            _format_params,
            _delete_from_archive,
            _delete_from_db
            ]
            )
