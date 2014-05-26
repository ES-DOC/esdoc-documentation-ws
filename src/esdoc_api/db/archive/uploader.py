import os
import sys

import pyesdoc
import utils_io



class _DocumentContextInfo(object):
    """Encapsulates document information."""
    def __init__(self, project, fpath):
        self.decoded = None
        self.encoding = fpath.split('.')[1]
        self.encodings = set([self.encoding] + utils_io.ENCODINGS)
        self.encoding_errors = []
        self.encoded = []
        self.fpath = fpath
        self.fpath_accepted = self.fpath.replace('ingested', 'ingested_accepted')
        self.fpath_rejected = self.fpath.replace('ingested', 'ingested_rejected')
        self.is_accepted = os.path.exists(self.fpath_accepted)
        self.is_rejected = os.path.exists(self.fpath_rejected)
        self.id = None
        self.version = None


    def __repr__(self):
        return "{0} :: {1} :: {2}".format(self.doc_type, self.project, self.fpath)


def _get_documents(throttle=0):
    """Yields documents for processing."""
    yielded = 0
    for project, filepath in _get_feed_entries():
        document = _DocumentInfo(project, filepath, yielded + 1)
        if not document.is_pulled:
            yielded = yielded + 1
            yield document

        # ... apply throttle
        if throttle and throttle == yielded:
            return


def _get_documents():
    """Yields documents for processing."""
    for doc in utils_io.get_documents('ingested', _DocumentContextInfo):
        if not doc.is_accepted and not doc.is_rejected:
            yield doc



def execute(throttle=0):
	"""Uploads document archive to db.

    :param int throttle: Limits number of documents to be uploaded.

	"""
    # Get ready.
    # _prepare()

    # Go!
	print("Hello Dolly !")
