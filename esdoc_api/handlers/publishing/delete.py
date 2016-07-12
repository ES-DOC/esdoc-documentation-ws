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
from esdoc_api import utils
from esdoc_api.utils import config



def _get_params():
    """Returns query parameter validation specification."""
    return {
        'document_id': {
            'required': True,
            'value_formatter': lambda v : v.lower()
        },
        'document_version': {
            'required' : True,
            'value_formatter': lambda v : v.lower()
        }
    }


class DocumentDeleteRequestHandler(tornado.web.RequestHandler):
    """Publishing delete document request handler.

    """
    def _parse_request_params(self):
        """Parses url query parameters.

        """
        utils.up.parse(self, _get_params())


    def _delete_from_archive(self):
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


    def delete(self):
        """HTTP DELETE handler.

        """
        utils.h.invoke(self, (
            self._parse_request_params,
            self._delete_from_archive,
            self._delete_from_db
            ))
