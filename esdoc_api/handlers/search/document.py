# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import pyesdoc

from esdoc_api import constants
from esdoc_api import db
from esdoc_api.handlers.search import document_by_drs
from esdoc_api.handlers.search import document_by_external_id
from esdoc_api.handlers.search import document_by_id
from esdoc_api.handlers.search import document_by_name
from esdoc_api.utils import config
from esdoc_api.utils.http import HTTPRequestHandler
from esdoc_api.utils.http import HTTP_HEADER_Access_Control_Allow_Origin



# Default document encoding.
_DEFAULT_ENCODING = pyesdoc.ENCODING_JSON

# Map of search types to sub-handlers.
_SUB_HANDLERS = {
    "drs": document_by_drs,
    "externalid": document_by_external_id,
    "id": document_by_id,
    "name": document_by_name,
}

# Set of child document types to be reloaded from archive.
_CHILD_DOC_RELOAD_TYPES = tuple({
    pyesdoc.ontologies.cim.v1.software.ModelComponent
})


# Query parameter names.
_PARAM_CLIENT = 'client'
_PARAM_ENCODING = 'encoding'
_PARAM_PROJECT = 'project'
_PARAM_SEARCH_TYPE = 'searchType'


# Query parameter validation schema.
_REQUEST_VALIDATION_SCHEMA = {
    _PARAM_CLIENT: {
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_ENCODING: {
        'allowed_case_insensitive': pyesdoc.ENCODINGS_ALL,
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_PROJECT: {
        'allowed_case_insensitive': [p['name'] for p in constants.PROJECT],
        'required': True,
        'type': 'list', 'items': [{'type': 'string'}]
    },
    _PARAM_SEARCH_TYPE: {
        'allowed': _SUB_HANDLERS.keys(),
        'required': False,
        'type': 'list', 'items': [{'type': 'string'}]
    }
}


class DocumentSearchRequestHandler(HTTPRequestHandler):
    """Document search request handler.

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
            self.client = self.get_argument(_PARAM_CLIENT)
            self.encoding = self.get_argument(_PARAM_ENCODING)
            self.project = self.get_argument(_PARAM_PROJECT)
            self.searchType = self.get_argument(_PARAM_SEARCH_TYPE)
            sub_handler.decode_request(self)


        def _format_params():
            """Formats request.

            """
            self.client = self.client.lower()
            self.encoding = self.encoding.lower()
            self.project = self.project.lower()
            self.searchType = self.searchType.lower()
            try:
                sub_handler.format_params(self)
            except AttributeError:
                pass

        def _validate_params():
            """Performs further request validation.

            """
            try:
                sub_handler.validate_params(self)
            except AttributeError:
                pass


        def _exec_search():
            """Performs document search against db.

            """
            db.session.start(config.db)
            self.docs = [i for i in sub_handler.do_search(self) if i]


        def _read_docs_from_archive():
            """Reads documents from pyesdoc archive.

            """
            self.docs = [pyesdoc.archive.read(i.uid, i.version) for i in self.docs]
            self.docs = [i for i in self.docs if i]


        def _set_child_docs():
            """Sets child documents derived from main documents.

            """
            self.child_docs = []
            for doc in self.docs:
                self.child_docs += doc.ext.children


        def _override_main_docs():
            """Overrides main documents with child documents.

            """
            for child in self.child_docs:
                for doc in self.docs:
                    if type(doc) == type(child) and doc.meta.id == child.meta.id:
                        self.docs.remove(doc)


        def _reload_child_docs():
            """Reloads child documents from archive.

            """
            reloadable = [i for i in self.child_docs if isinstance(i, _CHILD_DOC_RELOAD_TYPES)]
            if not reloadable:
                return

            for doc in reloadable:
                self.child_docs.remove(doc)
                new_doc_version = doc.meta.version
                while pyesdoc.archive.exists(doc.meta.id, new_doc_version):
                    new_doc_version += 1
                new_doc = pyesdoc.archive.read(doc.meta.id, new_doc_version - 1)
                self.child_docs.append(new_doc)


        def _set_docs_for_output():
            """Sets final collection to be encoded.

            """
            # HTML documents require a sorted merge.
            if self.encoding == pyesdoc.ENCODING_HTML:
                self.docs = self.docs + self.child_docs
                self.docs = sorted(self.docs, key=lambda d: d.meta.sort_key)


        def _encode_docs():
            """Encodes documents loaded from pyesdoc archive.

            """
            # N.B. Tornado auto-encodes dict's to json.
            if self.encoding != pyesdoc.ENCODING_JSON:
                self.docs = pyesdoc.encode(self.docs, self.encoding)
            else:
                self.docs = pyesdoc.encode(self.docs, pyesdoc.ENCODING_DICT)


        def _set_output():
            """Sets output data to be returned to client.

            """
            # Set encoding.
            self.output_encoding = self.encoding

            # No documents.
            if not len(self.docs):
                self.output = None

            # Multiple html documents - already wrapped by pyesdoc.
            elif self.encoding == pyesdoc.ENCODING_HTML:
                self.output = "<div>{0}</div>".format(self.docs[0])
                # self.output = "<div>{0}</div>".format(self.docs)

            # Single document.
            elif len(self.docs) == 1:
                self.output = self.docs[0]

            # Multiple json documents - create wrapper.
            elif self.encoding == pyesdoc.ENCODING_JSON:
                self.output = {
                    'documents': self.docs
                }

            # Multiple xml documents - create wrapper.
            elif self.encoding == pyesdoc.ENCODING_XML:
                self.output = "<documents>{0}</documents>".format("".join(self.docs))


        # Validate default query parameters.
        if self.validate(_REQUEST_VALIDATION_SCHEMA, {'allow_unknown': True}):
            # Set sub-handler.
            sub_handler = _SUB_HANDLERS[self.get_argument(_PARAM_SEARCH_TYPE)]

            # Set full request validation schema.
            schema = _REQUEST_VALIDATION_SCHEMA.copy()
            schema.update(sub_handler.REQUEST_VALIDATION_SCHEMA)

            # Invoke request processing taskset.
            self.invoke(schema, [
                _decode_request,
                _format_params,
                _validate_params,
                _exec_search,
                _read_docs_from_archive,
                _set_child_docs,
                _override_main_docs,
                _reload_child_docs,
                _set_docs_for_output,
                _encode_docs,
                _set_output
                ])
