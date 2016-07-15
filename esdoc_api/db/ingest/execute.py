# -*- coding: utf-8 -*-
"""
.. module:: execute.py
   :platform: Unix
   :synopsis: Executes ingestion process from document archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import datetime, os
from multiprocessing import Pool

import pyesdoc
from pyesdoc import archive

from esdoc_api.db.ingest import set_drs
from esdoc_api.db.ingest import set_is_latest
from esdoc_api.db.ingest import set_external_id
from esdoc_api.db.ingest import set_primary
from esdoc_api.db.ingest import set_sub_project
from esdoc_api.db.ingest import validate
from esdoc_api.utils import config
from esdoc_api.utils import logger



# Error file template.
_ERROR = """
------------------------------------------------------------
ES-DOC INGEST ERROR @ {0}
------------------------------------------------------------
An error occurred whilst ingesting a document from the archive:

PROJECT = {1};
SOURCE = {2};
FILE NAME = {3};
FILE PATH = {4};
ERROR TYPE = {5};
ERROR = {6}.

"""


class _DocumentProcessingInfo(object):
    """Encapsulates document processing information.

    """
    def __init__(self, file_, index):
        """Object constructor.

        """
        self.doc = None
        self.file = file_
        self.error = None
        self.index = index


    def __repr__(self):
        """Object representation.

        """
        if self.file:
            return "Processing ID = {} :: File = {}".format(
                self.index,
                self.file.path
                )
        elif self.doc:
            return "Processing ID = {} :: Doc = {}::{}".format(
                self.index,
                self.doc.meta.id,
                self.doc.meta.version,
                )
        else:
            return "Processing ID = {}".format(self.index)


    @property
    def folder(self):
        """Gets folder with which file is associated.

        """
        return self.file.folder

    @property
    def project(self):
        """Gets project with which file is associated.

        """
        return self.file.project

    @property
    def source(self):
        """Gets source with which file is associated.

        """
        return self.file.source


def _write_to_archive(ctx):
    """Archives document.

    """
    if ctx.doc is None:
        return

    folder = pyesdoc.archive.get_folder(ctx.doc.meta.project, ctx.doc.meta.source, True)
    fpath = pyesdoc.write(ctx.doc, folder.path)

    


def _set_document(ctx):
    """Sets document to be processed.

    """
    if ctx.doc is not None:
        return

    ctx.doc = ctx.file.get_document()


def _log(msg):
    """Writes a log message.

    """
    logger.log("INDEXING :: {0} ...".format(msg))


def _log_error(ctx):
    """Write processing error message to standard output.

    """
    # Escape if processing a controlled loop exit.
    if isinstance(ctx.error, StopIteration):
        return

    msg = "INGEST ERROR :: {0} :: {1} :: {2}"
    msg = msg.format(ctx, type(ctx.error), ctx.error)
    logger.log(msg)


def _write_error(ctx):
    """Writes document processing error to file system.

    """
    # Escape if processing a controlled loop exit.
    if isinstance(ctx.error, StopIteration):
        _rename_document(ctx)
        return

    try:
        with open(ctx.file.path_error, 'wb') as output:
            output.seek(0)
            output.write(_ERROR.format(
                datetime.datetime.now(),
                ctx.project,
                ctx.source,
                ctx.file.name,
                ctx.file.path,
                type(ctx.error),
                ctx.error
                ))
    except IOError:
        _log("Document processing error handling failed.")


def _rename_document(ctx):
    """Renames a document once ingestion has occurred.

    """
    new_path = "{0}_{1}_{2}_{3}.{4}".format(
        ctx.doc.meta.type.replace(".", "-"),
        ctx.doc.meta.id,
        ctx.doc.meta.version,
        ctx.file.hashid,
        ctx.file.encoding
        )
    new_path = os.path.join(ctx.folder.path, new_path.lower())
    if not os.path.exists(new_path):
        os.rename(ctx.file.path, new_path)


def _yield_documents(cfg):
    """Yields documents for processing.

    """
    yielded = 0
    for project in cfg.projects.split(","):
        project = project.strip().lower()
        for fwrapper in archive.yield_files(project, "*", None):
            yielded += 1
            yield _DocumentProcessingInfo(fwrapper, yielded)
            if cfg.throttle and cfg.throttle == yielded:
                break


def _invoke(ctx, tasks, error_tasks):
    """Invokes a set of actions.

    """
    try:
        for task in tasks:
            task(ctx)
    except Exception as exc:
        ctx.error = exc
        for task in error_tasks:
            task(ctx)


def _process(ctx):
    """Ingests a document.

    """
    tasks = (
        _write_to_archive,
        _set_document,
        validate.execute,
        set_primary.execute,
        set_is_latest.execute,
        set_sub_project.execute,
        set_drs.execute,
        set_external_id.execute,
        _rename_document,
        )

    error_tasks = (
        _log_error,
        _write_error
        )

    _invoke(ctx, tasks, error_tasks)


def _process_all():
    """Ingests all files from archive.

    """
    archive.init()
    archive.delete_error_files()
    if config.ingestion.parallelize:
        pool = Pool()
        pool.map(_process, _yield_documents(config.ingestion))
    else:
        for ctx in _yield_documents(config.ingestion):
            _process(ctx)


def execute(doc=None):
    """Ingests from archive.

    """
    if doc is None:
        _process_all()
    else:
        ctx = _DocumentProcessingInfo(None, 1)
        ctx.doc = doc
        _process(ctx)
