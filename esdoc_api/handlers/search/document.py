# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

import pyesdoc

from esdoc_api import db, utils
from esdoc_api.utils import config
from esdoc_api.handlers.search import (
    document_by_drs,
    document_by_external_id,
    document_by_id,
    document_by_name
    )



# Default document encoding.
_DEFAULT_ENCODING = pyesdoc.ESDOC_ENCODING_JSON

# Map of search types to sub-handlers.
_SUB_HANDLERS = {
    "drs": document_by_drs,
    "externalid": document_by_external_id,
    "id": document_by_id,
    "name": document_by_name,
}

# Set of child document types to be reloaded from archive.
_CHILD_DOC_RELOAD_TYPES = {
    pyesdoc.ontologies.cim.v1.software.ModelComponent
}


def _get_default_params():
    """Returns default document search parameter specification.

    """
    return {
        'encoding': {
            'required': True,
            'model_type': db.models.DocumentEncoding,
            'value_formatter': lambda v : v.lower()
        },
        'language': {
            'required': True,
            'model_type': db.models.DocumentLanguage,
            'value_formatter': lambda v : v.lower()
        },
        'onJSONPLoad': {
            'required' : False,
        },
        'ontology': {
            'required': True,
            'model_type': db.models.DocumentOntology,
            'value_formatter': lambda v : v.lower()
        },
        'project': {
            'required': True,
            'model_type': db.models.Project,
            'value_formatter': lambda v : v.lower(),
        },
        'searchType': {
            'required': True,
            'whitelist': _SUB_HANDLERS.keys(),
            'value_formatter': lambda v : v.lower()
        },
        'timestamp': {
            'required': False
        },
    }


class DocumentSearchRequestHandler(tornado.web.RequestHandler):
    """Document search request handler.

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

        # Load cache.
        db.cache.load()


    def _parse_params_default(self):
        """Parses url parameters common to all search types.

        """
        params = _get_default_params()
        utils.up.parse(self, params, apply_whitelist=False)


    def _set_sub_handler(self):
        """Sets search sub-handler.

        """
        self.sub_handler = _SUB_HANDLERS[self.search_type]


    def _parse_params_custom(self):
        """Parses search type specific url parameters.

        """
        # Set params to be parsed.
        params = _get_default_params()
        params.update(self.sub_handler.get_url_params())

        # Do standard parsing.
        utils.up.parse(self, params)

        # Do sub-handler specific parsing.
        try:
            self.sub_handler.parse_url_params(self)
        except AttributeError:
            pass


    def _do_search(self):
        """Performs document search against db.

        """
        self.docs = [d for d in self.sub_handler.do_search(self)
                     if d is not None]


    def _read_docs_from_archive(self):
        """Reads documents from pyesdoc archive.

        """
        self.docs =  [pyesdoc.archive.read(d.UID, d.Version) for d in self.docs]
        self.docs = [d for d in self.docs if d is not None]


    def _set_child_docs(self):
        """Sets child documents derived from main documents.

        """
        self.child_docs = []
        for doc in self.docs:
            self.child_docs += doc.ext.children


    def _override_main_docs(self):
        """Overrides main documents with child documents.

        """
        for child in self.child_docs:
            for doc in self.docs:
                if type(doc) == type(child) and doc.meta.id == child.meta.id:
                    self.docs.remove(doc)


    def _reload_child_docs(self):
        """Reloads child documents from archive.

        """
        reloadable = [d for d in self.child_docs if isinstance(d, tuple(_CHILD_DOC_RELOAD_TYPES))]
        if not reloadable:
            return

        for doc in reloadable:
            self.child_docs.remove(doc)
            new_doc_version = doc.meta.version
            while pyesdoc.archive.exists(doc.meta.id, new_doc_version):
                new_doc_version += 1
            new_doc = pyesdoc.archive.read(doc.meta.id, new_doc_version - 1)
            self.child_docs.append(new_doc)


    def _set_docs_for_output(self):
        """Sets final collection to be encoded.

        """
        # Set target encoding.
        encoding = self.encoding.Encoding

        # HTML documents require a sorted merge.
        if encoding == pyesdoc.ESDOC_ENCODING_HTML:
            self.docs = self.docs + self.child_docs
            self.docs = sorted(self.docs, key=lambda d: d.meta.sort_key)


    def _encode_docs(self):
        """Encodes documents loaded from pyesdoc archive.

        """
        # N.B. Tornado auto-encodes dict's to json.
        if self.encoding.Encoding != pyesdoc.ESDOC_ENCODING_JSON:
            self.docs =  pyesdoc.encode(self.docs, self.encoding.Encoding)
        else:
            self.docs =  pyesdoc.encode(self.docs, pyesdoc.ESDOC_ENCODING_DICT)


    def _set_response(self):
        """Sets response.

        """
        # Set encoding.
        self.output_encoding = encoding = self.encoding.Encoding


        # No documents.
        if not len(self.docs):
            self.output = None

        # Multiple html documents - already wrapped by pyesdoc.
        elif encoding == pyesdoc.ESDOC_ENCODING_HTML:
            self.output = "<div>{0}</div>".format(self.docs[0])
            # self.output = "<div>{0}</div>".format(self.docs)

        # Single document.
        elif len(self.docs) == 1:
            self.output = self.docs[0]

        # Multiple json documents - create wrapper.
        elif encoding == pyesdoc.ESDOC_ENCODING_JSON:
            self.output = {
                'documents': self.docs
            }

        # Multiple xml documents - create wrapper.
        elif encoding == pyesdoc.ESDOC_ENCODING_XML:
            self.output = "<documents>{0}</documents>".format("".join(self.docs))



    def get(self):
        """HTTP GET handler.

        """
        utils.h.invoke(self, (
            self._parse_params_default,
            self._set_sub_handler,
            self._parse_params_custom,
            self._do_search,
            self._read_docs_from_archive,
            self._set_child_docs,
            self._override_main_docs,
            self._reload_child_docs,
            self._set_docs_for_output,
            self._encode_docs,
            self._set_response
            ))
