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
from esdoc_api.utils import convert




def _get_params():
    """Returns url parameter specification."""
    return dict()


def _load(mtype, sort_key=None):
    """Helper function to load a collection from db.

    """
    collection = db.cache.get(mtype)
    collection = db.models.to_dict_for_json(collection)
    if sort_key:
        collection = sorted(collection, key=lambda i: i[sort_key].lower())

    return collection


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

        # Load db.cache.
        db.cache.load()

        # Parse incoming url parameters.
        utils.up.parse(self, _get_params())


    def _set_output(self):
        """Sets output data to be returned to client.

        """
        self.output_encoding = 'json'
        self.output = {
            'projects' : _load(db.models.Project, sort_key='name'),
            'models' : db.dao.get_summary_model_set(),
            'experiments' : db.dao.get_summary_eperiment_set(),
            'institutes' : _load(db.models.Institute),
            'instituteCounts' : db.dao.get_project_institute_counts(),
            'documentTypes' : [convert.dict_keys_to_camel_case(dt) for dt in constants.DOCUMENT_TYPES],
            'documentTypeCounts' : db.dao.get_project_document_type_counts()
        }


    def get(self):
        """HTTP GET handler.

        """
        utils.h.invoke(self, self._set_output)
