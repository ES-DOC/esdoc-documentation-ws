# -*- coding: utf-8 -*-
"""
.. module:: execute.py
   :platform: Unix
   :synopsis: Executes ingestion process from document archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime, os

import pyesdoc

from esdoc_api.db.ingest import (
    set_drs,
    set_external_id,
    set_is_latest,
    set_primary,
    set_summary,
    validate
    )
from esdoc_api.utils import runtime as rt


class _DocumentProcessingInfo(object):
    """Encapsulates document processing information.

    """
    def __init__(self,
                 organized,
                 ingestable,
                 index,
                 doc=None):
        """Object constructor.

        """
        self.doc = doc
        self.error = None
        self.fpath_error = ingestable.path.replace("ingested", "ingested_error")
        self.index = index
        self.ingestable = ingestable
        self.organized = organized


    def __repr__(self):
        """Object representation.

        """
        return "Processing ID = {0} :: Doc ID = {1} :: Doc Version = {2}".format(
            self.index,
            self.doc.meta.id,
            self.doc.meta.version)


class _DecodingException(Exception):
    """Exception raised when document decoding fails.

    """
    pass


class _ExtendingException(Exception):
    """Exception raised when document extension fails.

    """
    pass


def _set_document(ctx):
    """Sets document prior to processing.

    """
    if not ctx.doc:
        try:
            ctx.doc = pyesdoc.read(ctx.organized.path, ctx.organized.encoding)
        except Exception as err:
            raise _DecodingException(err)

    if not hasattr(ctx.doc, 'ext'):
        try:
            pyesdoc.extend(ctx.doc)
        except Exception as err:
            raise _ExtendingException(err)


def _write_error(ctx):
    """Writes document processing error to file system.

    """
    # Escape if writing controlled loop exit errors.
    if isinstance(ctx.error, StopIteration):
        return

    # Create error file.
    try:
        with open(ctx.fpath_error, 'wb') as output:
            output.seek(0)
            output.write(u"------------------------------------------------------------\n")
            output.write(u"ES-DOC API DB INGEST ERROR @ {} \n".format(datetime.datetime.now()))
            output.write(u"------------------------------------------------------------\n")
            output.write(u"An error occurred whilst ingesting a document:\n\n")
            output.write(u"\tPROJECT = {0};\n".format(ctx.doc.meta.project))
            output.write(u"\tSOURCE = {0};\n".format(ctx.doc.meta.source))
            output.write(u"\tFILEPATH = {0};\n".format(ctx.organized.path))
            output.write(u"\tERROR = {0};\n".format(unicode(ctx.error)))
            output.write(u"\tERROR TYPE = {0}.".format(type(ctx.error)))
    except IOError as err:
        rt.log_warning("Document processing error handler failed: {0}".format(err))


def _log_error(ctx):
    """Write processing error message to standard output.

    """
    # Escape if writing controlled loop exit errors.
    if isinstance(ctx.error, StopIteration):
        return

    rt.log("INGEST ERROR :: {0} :: {1} :: {2}".format(ctx, ctx.error, type(ctx.error)))


def _write_ingested(ctx):
    """Writes ingested file to archive.

    """
    # Escape if file already exists.
    if ctx.ingestable.exists:
        return

    # Escape upon uncontrolled error.
    if ctx.error and not isinstance(ctx.error, StopIteration):
        return

    # Create symbolic link to organized file.
    os.symlink(ctx.organized.path, ctx.ingestable.path)


def _get_documents(throttle=0):
    """Yields documents for processing.

    """
    yielded = 0
    for organized, ingestable in pyesdoc.archive.yield_ingestable():
        yielded += 1
        yield _DocumentProcessingInfo(organized, ingestable, yielded)
        if throttle and throttle == yielded:
            break


def _process(ctx):
    """Ingests a document.

    """
    tasks = (
        _set_document,
        validate.execute,
        set_primary.execute,
        set_is_latest.execute,
        set_summary.execute,
        set_drs.execute,
        set_external_id.execute,
        _write_ingested
        )

    error_tasks = (
        _write_ingested,
        _write_error,
        _log_error
        )

    rt.invoke(ctx, tasks, error_tasks)


def process_doc(doc):
    """Ingests a single document.

    """
    organized = \
        pyesdoc.archive.get_doc_file(doc, pyesdoc.archive.DIR_ORGANIZED)
    ingestable = \
        pyesdoc.archive.get_doc_file(doc, pyesdoc.archive.DIR_INGESTED)

    _process(_DocumentProcessingInfo(organized, ingestable, 1, doc))


def process_archived(throttle=0):
    """Ingests files from archive.

    :param int throttle: Limits the number of documents to process.

    """
    pyesdoc.archive.delete_files(pyesdoc.archive.DIR_INGESTED_ERROR)
    for ctx in _get_documents(throttle):
        _process(ctx)
