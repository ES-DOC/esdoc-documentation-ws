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
from esdoc_api.utils.http import process_request



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
            self.doc_id = self.get_argument(_PARAM_DOCUMENT_ID).lower()
            self.doc_version = self.get_argument(_PARAM_DOCUMENT_VERSION).lower()


        def _delete_from_archive():
            """Deletes document from archive.

            """
            pyesdoc.archive.delete(self.doc_id, self.doc_version)


        def _delete_from_db(self):
            """Deletes document from database.

            """
            # TODO switch to context manager
            # with db.session.start():
            #     db.ingest.undo(self.doc_id, self.doc_version)

            db.session.start(config.db)
            try:
                db.ingest.undo(self.doc_id, self.doc_version)
                db.session.commit()
            finally:
                db.session.end()


        # Process request.
        process_request(self, [
            _set_criteria,
            _delete_from_archive,
            _delete_from_db
            ])
