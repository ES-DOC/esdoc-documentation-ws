# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.summary.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document summary search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import constants
from esdoc_api import db
from esdoc_api.db.dao import get_document_summaries
from esdoc_api.db.dao import get_document_type_count
from esdoc_api.utils import config
from esdoc_api.utils.http import HTTPRequestHandler
from esdoc_api.utils.http import HTTP_HEADER_Access_Control_Allow_Origin



# Query parameter names.
_PARAM_TIMESTAMP = 'timestamp'
_PARAM_DOCUMENT_TYPE = 'documentType'
_PARAM_DOCUMENT_VERSION = 'documentVersion'
_PARAM_EXPERIMENT = 'experiment'
_PARAM_INSTITUTE = 'institute'
_PARAM_MODEL = 'model'
_PARAM_PROJECT = 'project'
_PARAM_SUB_PROJECT = 'subProject'

# Query parameter validation schema.
_REQUEST_VALIDATION_SCHEMA = {
    _PARAM_TIMESTAMP: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_DOCUMENT_TYPE: {
        'allowed_case_insensitive': [i['key'] for i in constants.DOCUMENT_TYPES],
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_DOCUMENT_VERSION: {
        'allowed': constants.DOCUMENT_VERSIONS,
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_EXPERIMENT: {
        'required': False,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_INSTITUTE: {
        'required': False,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_MODEL: {
        'required': False,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_PROJECT: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_SUB_PROJECT: {
        'required': False,
        'type': 'list', 'items': [{'type': 'string'}]
    }
}


class SummarySearchRequestHandler(HTTPRequestHandler):
    """Document summary search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request.

        """
        self.set_header(HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def get(self):
        """HTTP GET handler.

        """
        def _decode_request():
            """Decodes request.

            """
            self.timestamp = self.get_argument(_PARAM_TIMESTAMP)
            self.document_type = self.get_argument(_PARAM_DOCUMENT_TYPE)
            self.document_version = self.get_argument(_PARAM_DOCUMENT_VERSION)
            self.experiment = self.get_argument(_PARAM_EXPERIMENT, None)
            self.institute = self.get_argument(_PARAM_INSTITUTE, None)
            self.model = self.get_argument(_PARAM_MODEL, None)
            self.project = self.get_argument(_PARAM_PROJECT)
            self.sub_project = self.get_argument(_PARAM_SUB_PROJECT, None)


        def _format_params():
            """Formats request parameters.

            """
            self.document_type = self.document_type.lower()
            if self.institute:
                self.institute = self.institute.lower()
            if self.project:
                self.project = self.project.lower()
            if self.sub_project:
                self.sub_project = self.sub_project.lower()


        def _set_data():
            """Pulls data from db.

            """
            # TODO- context manager
            db.session.start(config.db)

            self.data = get_document_summaries(
                self.project,
                self.document_type,
                self.document_version,
                sub_project=self.sub_project,
                institute=self.institute,
                model=self.model or None,
                experiment=self.experiment or None
                )
            self.total = get_document_type_count(self.project, self.document_type)


        def _set_output():
            """Sets output data to be returned to client.

            """
            self.output = {
                'count': len(self.data),
                'project': self.project,
                'results': self.data,
                'timestamp': self.timestamp,
                'total': self.total
            }


        self.invoke(_REQUEST_VALIDATION_SCHEMA, [
            _decode_request,
            _format_params,
            _set_data,
            _set_output
            ]
            )
