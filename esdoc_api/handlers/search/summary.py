# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.summary.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document summary search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api import constants
from esdoc_api import db
from esdoc_api import utils
from esdoc_api.utils import config



def _get_params():
    """Returns url parameter specification."""
    return {
        'timestamp': {
            'required': True
        },
        'documentType': {
            'required': True,
            'whitelist' : [dt['key'].lower() for dt in constants.DOCUMENT_TYPES],
            'value_formatter': lambda v: v.lower()
        },
        'documentVersion': {
            'required': True,
            'whitelist': lambda: constants.DOCUMENT_VERSIONS
        },
        'experiment': {
            'required': False
        },
        'institute': {
            'required': False,
            'value_formatter': lambda v: v.lower()
        },
        'model': {
            'required': False
        },
        'project': {
            'required': True,
            'value_formatter': lambda v: v.lower(),
        }
    }


def _get_collection(mtype):
    """Helper function to load collection from db.

    """
    return db.models.to_dict_for_json(db.dao.get_all(mtype))


class SummarySearchRequestHandler(tornado.web.RequestHandler):
    """Document summary search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request."""
        self.set_header(utils.h.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def prepare(self):
        """Prepare handler state for processing."""
        # Start db session.
        db.session.start(config.db)


    def _parse_params(self):
        """Parses incoming url parameters."""
        utils.up.parse(self, _get_params())


    def _set_data(self):
        """Sets data returned from db."""
        self.data = db.dao.get_document_summaries(
            self.project,
            self.document_type,
            self.document_version,
            self.institute,
            self.model if self.model else None,
            self.experiment if self.experiment else None
            )


    def _set_total(self):
        """Sets total of all records returnable from db."""
        self.total = \
            db.dao.get_document_type_count(self.project, self.document_type)


    def _set_output(self):
        """Sets output data to be returned to client."""
        self.output_encoding = 'json'
        self.output = {
            'count': len(self.data),
            'project': self.project,
            'results': self.data,
            'timestamp': self.timestamp,
            'total': self.total
        }



    def get(self):
        """HTTP GET handler."""
        utils.h.invoke(self, (
            self._parse_params,
            self._set_data,
            self._set_total,
            self._set_output
            ))
