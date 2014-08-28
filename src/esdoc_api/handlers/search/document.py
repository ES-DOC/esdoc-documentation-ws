# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

import pyesdoc
from pyesdoc.db import (
    cache,
    models,
    session
    )

from ... import utils

from . import (
    document_by_drs,
    document_by_external_id,
    document_by_id,
    document_by_name
    )



# Map of search types to sub-handlers.
_SUB_HANDLERS = {
    "drs": document_by_drs,
    "externalid": document_by_external_id,
    "id": document_by_id,
    "name": document_by_name,
}


def _get_default_params():
    """Returns default document search parameter specification."""
    return {
        'encoding': {
            'required': True,
            'model_type': models.DocumentEncoding,
            'value_formatter': lambda v : v.lower()
        },
        'language': {
            'required': True,
            'model_type': models.DocumentLanguage,
            'value_formatter': lambda v : v.lower()
        },
        'onJSONPLoad': {
            'required' : False,
        },
        'ontology': {
            'required': True,
            'model_type': models.DocumentOntology,
            'value_formatter': lambda v : v.lower()
        },
        'project': {
            'required': True,
            'model_type': models.Project,
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


def _format_docs(docs, encoding):
    """Helper function to format documents."""

    def set_html():
        """HTML formatter."""
        result = "<div class='esdoc-document-set'>{0}</div>"
        result = result.format("".join(docs))

        return result

    def set_json():
        """JSON formatter."""
        return {
            'documents': docs
        }

    def set_xml():
        """XML formatter."""
        return "<documents>{0}</documents>".format("".join(docs))

    # No documents.
    if not len(docs):
        return None

    # Single document.
    elif len(docs) == 1:
        return docs[0]

    # Multiple html documents.
    elif encoding == pyesdoc.ESDOC_ENCODING_HTML:
        return set_html()

    # Multiple html documents.
    elif encoding == pyesdoc.ESDOC_ENCODING_JSON:
        return set_json()

    # Multiple html documents.
    elif encoding == pyesdoc.ESDOC_ENCODING_XML:
        return set_xml()

    # Other error.
    else:
        raise ValueError("Unsupported encoding [{0}].".format(encoding))


class DocumentSearchRequestHandler(tornado.web.RequestHandler):
    """Document search request handler.

    """
    def set_default_headers(self):
        """Set HTTP headers at the beginning of the request."""
        self.set_header(utils.h.HTTP_HEADER_Access_Control_Allow_Origin, "*")


    def prepare(self):
        """Prepare handler state for processing."""
        # Start db session.
        session.start(utils.config.db.connection)

        # Load cache.
        cache.load()


    def _parse_default_params(self):
        """Parses url parameters common to all search types."""
        params = _get_default_params()
        utils.up.parse(self, params, apply_whitelist=False)


    def _set_sub_handler(self):
        """Sets search sub-handler."""
        self.sub_handler = _SUB_HANDLERS[self.search_type]


    def _parse_custom_params(self):
        """Parses search type specific url parameters."""
        # Set params to be parsed.
        params = _get_default_params()
        params.update(self.sub_handler.get_url_params())

        # Do standard parsing.
        utils.up.parse(self, params)

        # Do sub-handler specific parsing.
        if hasattr(self.sub_handler, "parse_url_params"):
            self.sub_handler.parse_url_params(self)


    def _do_search(self):
        """Performs document search against db."""
        self.docs = [d for d in self.sub_handler.do_search(self) if d]


    def _load_docs(self):
        """Loads documents from pyesdoc archive."""

        def load(doc):
            """Loads a document."""
            document = pyesdoc.archive.get(doc.UID, doc.Version)
            if document:
                return document
            else:
                raise RuntimeError("""Document is indexed in db but no longer
                                      exists within archive.""")

        self.docs =  [load(d) for d in self.docs]


    def _encode_docs(self):
        """Encodes loaded documents."""
        # Escape if converting to default encoding.
        encoding = self.encoding.Encoding
        if encoding == pyesdoc.ESDOC_ENCODING_JSON:
            return

        def encode(doc):
            """Returns an encoded document."""
            doc = pyesdoc.decode(doc, pyesdoc.ESDOC_ENCODING_JSON)
            doc = pyesdoc.extend(doc)

            return pyesdoc.encode(doc, encoding)

        self.docs =  [encode(d) for d in self.docs]


    def _set_response(self):
        """Sets response."""
        self.output = _format_docs(self.docs, self.encoding.Encoding)
        self.output_encoding = self.encoding.Encoding


    def get(self):
        """HTTP GET handler."""
        utils.h.invoke(self, (
            self._parse_default_params,
            self._set_sub_handler,
            self._parse_custom_params,
            self._do_search,
            self._load_docs,
            self._encode_docs,
            self._set_response
            ))
