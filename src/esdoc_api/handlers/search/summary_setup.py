# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.summary_setup.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document summary search setup request handler.

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
            'required': False
        }
    }


def _load(mtype):
    """Helper function to load collection from db."""
    return models.to_dict_for_json(cache.get(mtype))


class SummarySearchSetupRequestHandler(tornado.web.RequestHandler):
    """Document summary search setup request handler.

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

        # Parse incoming url parameters.
        utils.up.parse(self, _get_params())


    def _set_output(self):
        """Sets output data to be returned to client."""
        self.output = {
            'projects' : _load(models.Project),
            'models' : dao.get_summary_model_set(),
            'experiments' : dao.get_summary_eperiment_set(),
            'institutes' : _load(models.Institute),
            'instituteCounts' : dao.get_project_institute_counts(),
            'documentTypes' : _load(models.DocumentType),
            'documentTypeCounts' : dao.get_project_document_type_counts(),
            'documentLanguages' : _load(models.DocumentLanguage)
        }


    def get(self):
        """HTTP GET handler."""
        utils.h.invoke(self, self._set_output)
