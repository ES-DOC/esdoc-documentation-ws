"""
.. module:: ingest.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Ingests documents from document feeds.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import datetime
import hashlib
import os
from multiprocessing.dummy import Pool as ThreadPool

import feedparser
import requests


import esdoc_api.lib.utils.runtime as rt
from . import utils_io



# Default document encoding.
_ENCODING = 'utf-8'

# Target folder to which downloaded files will be copied.
_TARGET_FOLDER = "pulled"


# Requests session.
_SESSION = None


class _DownloadException(Exception):
    """Exception raised when a download fails."""
    pass


class _EncodingException(Exception):
    """Exception raised when raw document encoding fails."""
    pass


class _IOException(Exception):
    """Exception raised when document io fails."""
    pass


class _DocumentInfo(object):
    """Encapsulates document information."""
    def __init__(self, project, url, encoding, index):
        self.content = None
        self.encoding = encoding
        self.error = None
        self.error_header = None
        self.filename = "{0}.{1}".format(hashlib.md5(url).hexdigest(), encoding)
        self.folder = utils_io.folders[project][_TARGET_FOLDER]
        self.folder_error = utils_io.folders[project][_TARGET_FOLDER + "_error"]
        self.folder_type = _TARGET_FOLDER
        self.id = index
        self.project = project
        self.url = url
        self.filepath = os.path.join(self.folder, self.filename)
        self.filepath_error = os.path.join(self.folder_error, self.filename)
        self.is_pulled = os.path.exists(self.filepath)


    def __repr__(self):
        return "{0} :: {1} :: {2} :: {3} :: {4}".format(
            self.folder_type, self.project, self.url, self.filename, self.is_pulled)


def _get_feeds():
    """Returns generator of active feeds."""
    for project in utils_io.config.projects:
        for feed in (f for f in project.feeds if f.is_active):
            msg = "ARCHIVE :: processing feed: {0} --> {1}"
            rt.log(msg.format(project.name, feed.url))
            yield project, feed


def _get_feed_entries():
    """Returns generator of active feeds."""
    for project, feed in _get_feeds():
        for entry in feedparser.parse(feed.url).entries:
            yield project.name, entry.links[0]['href'], feed.encoding


def _get_documents(throttle=0):
    """Yields documents for processing."""
    yielded = 0
    for project, url, encoding in _get_feed_entries():
        document = _DocumentInfo(project, url, encoding, yielded + 1)
        if not document.is_pulled:
            yielded = yielded + 1
            yield document

        # ... apply throttle
        if throttle and throttle == yielded:
            return


def _log_start(document):
    """Writes a processing start message to standard output."""
    msg = "ARCHIVE :: processing document {0}: {1} --> {2}"
    rt.log(msg.format(document.id, document.project, document.url))


def _pull(document):
    """Attempts to pull document from remote endpoint."""
    try:
        document.r = _SESSION.get(document.url)
    except Exception as err:
        raise _DownloadException(err)
    else:
        if document.r.status_code != 200:
            raise _DownloadException()


def _encode(document):
    """Encodes a downloaded document."""
    try:
        document.content = document.r.text.encode(_ENCODING)
    except Exception as err:
        raise _EncodingException(err)


def _persist(document):
    """Writes a downloaded document to the file system."""
    try:
        with open(document.filepath, 'w') as fpointer:
            fpointer.seek(0)
            fpointer.write(str(document.content))
    except IOError as err:
        raise _IOException(err)
    else:
        document.is_pulled = True


def _log_error(document):
    """Write processing error message to standard output."""
    msg = "ARCHIVE ERROR :: processing document {0}: {1} ---> {2}"
    msg = msg.format(document.id, document.project, document.error)
    rt.log(msg)


def _persist_error(document):
    """Persist document processing error to file system."""
    try:
        with open(document.filepath_error, 'wb') as fpointer:
            fpointer.seek(0)
            fpointer.write(u"------------------------------------------------------------\n")
            fpointer.write(u"ES-DOC ARCHIVE BUILD ERROR @ {} \n".format(datetime.datetime.now()))
            fpointer.write(u"------------------------------------------------------------\n")
            fpointer.write(u"An error occurred whilst pulling a document from a remote source:\n\n")
            fpointer.write(u"\tPROJECT = {0};\n".format(document.project))
            fpointer.write(u"\tDOCUMENT URL = {0};\n".format(document.url))
            fpointer.write(u"\tDOCUMENT ENCODING = {0};\n".format(document.encoding))
            fpointer.write(u"\tERROR = {0}.".format(unicode(document.error)))
    except IOError:
        rt.log("Document processing error handling failed.")


def _process(document):
    """Processes a downloaded document."""
    try:
        for func in (_log_start, _pull, _encode, _persist):
            func(document)
    except Exception as exc:
        document.error = exc
        for func in (_log_error, _persist_error):
            func(document)


def _prepare():
    """Performs execution preparation tasks."""
    # Initialise io.
    utils_io.init()

    # Clear error folder.
    utils_io.reset_sub_folder(_TARGET_FOLDER + "_error")

    # Initialize requests session with increaed connection pool size.
    global _SESSION
    _SESSION = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=100,
                                            pool_maxsize=100)
    _SESSION.mount('http://', adapter)


def execute(throttle=0):
    """Downloads documents from the set of atom feeds defined in config.json.

    :param int throttle: Limits number of documents to be pulled.

    """
    # Get ready.
    _prepare()

    # Go!
    pool = ThreadPool()
    pool.map(_process, _get_documents(throttle))
