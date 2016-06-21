# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.summary_setup.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document summary search setup request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

from esdoc_api import constants
from esdoc_api import db
from esdoc_api import utils
from esdoc_api.utils import config



class SummarySearchSetupRequestHandler(tornado.web.RequestHandler):
    """Document summary search setup request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(utils.h.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def prepare(self):
        """Prepare handler state for processing.

        """
        # Start db session.
        db.session.start(config.db)

        # Parse incoming url parameters.
        utils.up.parse(self)


    def _set_output(self):
        """Sets output data to be returned to client.

        """
        self.output_encoding = 'json'
        self.output = {
            'project' : db.dao.get_projects(),
            'documentType' : ["{}:{}".format(i[0], i[1]) for i in db.dao.get_document_types()],
            'documentVersion' : constants.DOCUMENT_VERSION,
            'institute' : ["{}:{}".format(i[0], i[1]) for i in db.dao.get_institutes()],
            'model' : ["{}:{}".format(i[0], i[1]) for i in db.dao.get_models()],
            'experiment' : ["{}:{}".format(i[0], i[1]) for i in db.dao.get_experiments()],
            'subProject' : ["{}:{}".format(i[0], i[1]) for i in db.dao.get_sub_projects()],
            'cv': {
                'documentTypes' : constants.DOCUMENT_TYPES,
            },
            'documentTypes' : constants.DOCUMENT_TYPES,
            'projects' : constants.PROJECT,
            'subProjects' : constants.SUB_PROJECT,
            'models' : db.dao.get_models(),
            'experiments' : db.dao.get_experiments(),
            'institutes': [i[1] for i in db.dao.get_institutes()],
            'instituteCounts' : db.dao.get_project_institute_counts(),
            'documentTypeCounts' : db.dao.get_project_document_type_counts()
        }


    def get(self):
        """HTTP GET handler.

        """
        utils.h.invoke(self, self._set_output)
