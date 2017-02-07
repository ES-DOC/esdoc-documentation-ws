# -*- coding: utf-8 -*-

"""
.. module:: handlers.search.document.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Document search request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import pyesdoc

from esdoc_api.utils.convertor import to_underscore_case



# Default query parameter names.
_DEFAULT_PARAMS = {
    'client',
    'encoding',
    'project'
}

# Default document encoding.
_DEFAULT_ENCODING = pyesdoc.constants.ENCODING_JSON

# Set of child document types to be reloaded from archive.
_CHILD_DOC_RELOAD_TYPES = tuple({
    pyesdoc.ontologies.cim.v1.software.ModelComponent
})


def parse_params(handler, params):
    """Parses incoming query parameters.

    """
    params = _DEFAULT_PARAMS.union(params)
    for param in params:
        formatter = lambda v: v
        if isinstance(param, tuple):
            param, formatter = param
        if handler.get_argument(param, None) in {None, "*"}:
            setattr(handler, to_underscore_case(param), None)
        else:
            setattr(handler, to_underscore_case(param), formatter(handler.get_argument(param)))


def set_output(handler, docs):
    """Sets response output derived from a document search.

    """
    ctx = _ProcessingContext(handler, docs)
    for func in [
        _init_docs,
        _read_docs_from_archive,
        _set_child_docs,
        _override_main_docs,
        _reload_child_docs,
        _set_docs_for_output,
        _encode_docs,
        _set_output
    ]:
        func(ctx)

    return ctx.docs


def _init_docs(ctx):
    """Initialises documents for processing.

    """
    try:
        iter(ctx.docs)
    except TypeError:
        ctx.docs = [ctx.docs]


def _read_docs_from_archive(ctx):
    """Reads documents from pyesdoc archive.

    """
    ctx.docs = [pyesdoc.archive.read(i.uid, i.version) for i in ctx.docs]
    ctx.docs = [i for i in ctx.docs if i]


def _set_child_docs(ctx):
    """Returns set of child documents derived from main documents.

    """
    for doc in ctx.docs:
        ctx.child_docs += doc.ext.children


def _override_main_docs(ctx):
    """Overrides main documents with child documents.

    """
    for child in ctx.child_docs:
        for doc in ctx.docs:
            if isinstance(doc, type(child)) and doc.meta.id == child.meta.id:
                ctx.docs.remove(doc)


def _reload_child_docs(ctx):
    """Reloads child documents from archive.

    """
    reloadable = [i for i in ctx.child_docs if isinstance(i, _CHILD_DOC_RELOAD_TYPES)]
    if not reloadable:
        return

    for doc in reloadable:
        ctx.child_docs.remove(doc)
        new_doc_version = doc.meta.version
        while pyesdoc.archive.exists(doc.meta.id, new_doc_version):
            new_doc_version += 1
        new_doc = pyesdoc.archive.read(doc.meta.id, new_doc_version - 1)
        ctx.child_docs.append(new_doc)


def _set_docs_for_output(ctx):
    """Sets final collection to be encoded.

    """
    # HTML documents require a sorted merge.
    if ctx.encoding == pyesdoc.constants.ENCODING_HTML:
        ctx.docs = ctx.docs + ctx.child_docs
        ctx.docs = sorted(ctx.docs, key=lambda d: d.meta.sort_key)


def _encode_docs(ctx):
    """Encodes documents loaded from pyesdoc archive.

    """
    if ctx.encoding != pyesdoc.constants.ENCODING_JSON:
        ctx.docs = pyesdoc.encode(ctx.docs, ctx.encoding)
    else:
        ctx.docs = pyesdoc.encode(ctx.docs, pyesdoc.ENCODING_DICT)


def _set_output(ctx):
    """Sets output data to be returned to client.

    """
    # Set encoding.
    ctx.handler.output_encoding = ctx.encoding

    # Null case.
    if len(ctx.docs) == 0:
        ctx.handler.output = None

    # Multiple html documents - already wrapped by pyesdoc.
    elif ctx.encoding == pyesdoc.constants.ENCODING_HTML:
        ctx.handler.output = "<div>{0}</div>".format(ctx.docs[0])
        # ctx.handler.output = "<div>{0}</div>".format(ctx.docs)

    # Single document.
    elif len(ctx.docs) == 1:
        ctx.handler.output = ctx.docs[0]

    # Multiple json documents - create wrapper.
    elif ctx.encoding == pyesdoc.constants.ENCODING_JSON:
        ctx.handler.output = {
            'documents': ctx.docs
        }

    # Multiple xml documents - create wrapper.
    elif ctx.encoding == pyesdoc.constants.ENCODING_XML:
        ctx.handler.output = "<documents>{0}</documents>".format("".join(ctx.docs))


class _ProcessingContext(object):
    """Processing context information wrapper.

    """
    def __init__(self, handler, docs):
        """Instance constructor.

        """
        self.child_docs = []
        self.docs = docs
        self.encoding = handler.encoding
        self.handler = handler

