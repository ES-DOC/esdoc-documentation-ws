# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.summary_setup.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document summary search setup request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api import db
from esdoc_api.utils import config
from esdoc_api.utils import constants
from esdoc_api.utils.http import process_request



class SummarySearchSetupRequestHandler(tornado.web.RequestHandler):
    """Document summary search setup request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(constants.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def get(self):
        """HTTP GET handler.

        """

        def _set_data():
            """Pulls data from db.

            """
            # TODO- context manager
            db.session.start(config.db)

            self.document_types = db.dao.get_document_types()
            self.experiments = db.dao.get_experiments()
            self.institutes = db.dao.get_institutes()
            self.models = db.dao.get_models()
            self.projects = db.dao.get_projects()
            self.sub_projects = db.dao.get_sub_projects()


        def _set_output():
            """Sets output data to be returned to client.

            """
            self.output = {
                'project' : self.projects,
                'documentType' : ["{}:{}".format(i[0], i[1]) for i in self.document_types],
                'documentVersion' : constants.DOCUMENT_VERSION,
                'institute' : ["{}:{}".format(i[0], i[1]) for i in self.institutes],
                'model' : ["{}:{}".format(i[0], i[1]) for i in self.models],
                'experiment' : ["{}:{}".format(i[0], i[1]) for i in self.experiments],
                'subProject' : ["{}:{}".format(i[0], i[1]) for i in self.sub_projects],
                'cv': {
                    'documentTypes' : constants.DOCUMENT_TYPES,
                }
            }


        # Process request.
        process_request(self, [
            _set_data,
            _set_output
            ])
