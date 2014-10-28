# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.summary.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document summary search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

from pyesdoc.db import (
    cache,
    dao,
    models,
    session
    )

from ... import utils
from ...utils import config


def _get_params():
    """Returns url parameter specification."""
    return {
        'onJSONPLoad': {
            'required': False
        },
        'timestamp': {
            'required': True
        },
        'documentLanguage': {
            'required': True,
            'model_type': models.DocumentLanguage,
            'value_formatter': lambda v : v.lower()
        },
        'documentType': {
            'required': True,
            'model_type': models.DocumentType,
            'value_formatter': lambda v : v.lower()
        },
        'documentVersion': {
            'required': True,
            'whitelist': lambda : models.DOCUMENT_VERSIONS
        },
        'experiment': {
            'required': False
        },
        'institute': {
            'required': False,
            'model_type': models.Institute,
            'value_formatter': lambda v : v.lower()
        },
        'model': {
            'required': False
        },
        'project': {
            'required': True,
            'model_type': models.Project,
            'value_formatter': lambda v : v.lower(),
        }
    }


def _get_collection(mtype):
    """Helper function to load collection from db."""
    return models.to_dict_for_json(dao.get_all(mtype))


class SummarySearchRequestHandler(tornado.web.RequestHandler):
    """Document summary search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request."""
        self.set_header(utils.h.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def prepare(self):
        """Prepare handler state for processing."""
        # Start db session.
        session.start(config.db)

        # Load cache.
        cache.load()


    def _parse_params(self):
        """Parses incoming url parameters."""
        utils.up.parse(self, _get_params())


    def _set_data(self):
        """Sets data returned from db."""
        self.data = dao.get_document_summaries(
            self.project.ID,
            self.document_type.Key,
            self.document_version,
            self.document_language.ID,
            self.institute.ID if self.institute else None,
            self.model if self.model else None,
            self.experiment if self.experiment else None)


    def _set_total(self):
        """Sets total of all records returnable from db."""
        self.total = \
            dao.get_document_type_count(self.project.ID,
                                        self.document_type.Key)


    def _set_output(self):
        """Sets output data to be returned to client."""
        self.output_encoding = 'json'
        self.output = {
            'count': len(self.data),
            'project': self.project.Name.lower(),
            'results': models.to_dict_for_json(self.data),
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
