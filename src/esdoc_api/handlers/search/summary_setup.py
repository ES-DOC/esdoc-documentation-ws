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

from esdoc_api import db, utils
from esdoc_api.utils import config



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
    return db.models.to_dict_for_json(db.cache.get(mtype))


class SummarySearchSetupRequestHandler(tornado.web.RequestHandler):
    """Document summary search setup request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request."""
        self.set_header(utils.h.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def prepare(self):
        """Prepare handler state for processing."""
        # Start db session.
        db.session.start(config.db)

        # Load db.cache.
        db.cache.load()

        # Parse incoming url parameters.
        utils.up.parse(self, _get_params())


    def _set_output(self):
        """Sets output data to be returned to client."""
        self.output_encoding = 'json'
        self.output = {
            'projects' : _load(db.models.Project),
            'models' : db.dao.get_summary_model_set(),
            'experiments' : db.dao.get_summary_eperiment_set(),
            'institutes' : _load(db.models.Institute),
            'instituteCounts' : db.dao.get_project_institute_counts(),
            'documentTypes' : _load(db.models.DocumentType),
            'documentTypeCounts' : db.dao.get_project_document_type_counts(),
            'documentLanguages' : _load(db.models.DocumentLanguage)
        }


    def get(self):
        """HTTP GET handler."""
        utils.h.invoke(self, self._set_output)
