# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.summary.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document summary search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api import db
from esdoc_api.db.dao import get_document_summaries
from esdoc_api.db.dao import get_document_type_count
from esdoc_api.utils import config
from esdoc_api.utils import constants
from esdoc_api.utils.http import process_request



# Query parameter names.
_PARAM_DOCUMENT_TYPE = 'document_type'
_PARAM_DOCUMENT_VERSION = 'document_version'
_PARAM_EXPERIMENT = 'experiment'
_PARAM_INSTITUTE = 'institute'
_PARAM_MODEL = 'model'
_PARAM_PROJECT = 'project'
_PARAM_SUB_PROJECT = 'sub_project'





class SummarySearchRequestHandler(tornado.web.RequestHandler):
    """Document summary search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Headers, "x-requested-with")
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Methods, 'POST, GET, OPTIONS')


    def get(self):
        """HTTP GET handler.

        """
        def _set_criteria():
            """Sets search criteria.

            """
            for param in {
                _PARAM_DOCUMENT_TYPE,
                _PARAM_DOCUMENT_VERSION,
                _PARAM_EXPERIMENT,
                _PARAM_INSTITUTE,
                _PARAM_MODEL,
                _PARAM_PROJECT,
                _PARAM_SUB_PROJECT
            }:
                if self.get_argument(param, None) in {None, "*"}:
                    setattr(self, param, None)
                else:
                    setattr(self, param, self.get_argument(param))


        def _set_data():
            """Pulls data from db.

            """
            # TODO- context manager
            db.session.start(config.db)

            self.summaries = get_document_summaries(
                self.project,
                self.document_type,
                self.document_version,
                sub_project=self.sub_project,
                institute=self.institute,
                model=self.model,
                experiment=self.experiment
                )
            self.total = get_document_type_count(self.project, self.document_type)


        def _set_output():
            """Sets output data to be returned to client.

            """
            self.output = {
                'count': len(self.summaries),
                'project': self.project,
                'results': self.summaries,
                'total': self.total
            }


        # Process request.
        process_request(self, [
            _set_criteria,
            _set_data,
            _set_output
            ])


    def options(self, *args):
        """HTTP OPTIONS handler.

        """        
        self.set_status(204)
        self.finish()
