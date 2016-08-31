# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.delete.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing delete document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

import pyesdoc

from esdoc_api import db
from esdoc_api.utils import config
from esdoc_api.utils1.http import process_request



# Query parameter names.
_PARAM_DOCUMENT_ID = 'document_id'
_PARAM_DOCUMENT_VERSION = 'document_version'


class DocumentDeleteRequestHandler(tornado.web.RequestHandler):
    """Publishing delete document request handler.

    """
    def delete(self):
        """HTTP DELETE handler.

        """
        def _set_criteria():
            """Sets search criteria.

            """
            for param in {
                _PARAM_DOCUMENT_ID,
                _PARAM_DOCUMENT_VERSION
            }:
                setattr(self, param, self.get_argument(param).lower())


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


        # Process request.
        process_request(self, [
            _set_criteria,
            _delete_from_archive,
            _delete_from_db
            ])
