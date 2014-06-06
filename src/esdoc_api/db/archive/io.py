"""
.. module:: utils_io.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: IO utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: utf-8 -*-

# Module imports.
import glob
import os
import shutil

import esdoc_api.pyesdoc.utils.convert as utils_conversion



# Archive folder.
_ARCHIVE_FOLDER = os.path.dirname(os.path.abspath(__file__))
for i in range(5):
    _ARCHIVE_FOLDER = os.path.dirname(_ARCHIVE_FOLDER)
_ARCHIVE_FOLDER = os.path.join(_ARCHIVE_FOLDER, "esdoc-archive")

# Documents folder.
_DOCS_FOLDER = os.path.join(_ARCHIVE_FOLDER, "documents")

# Configuration.
config = os.path.join(_ARCHIVE_FOLDER, "config.json")
config = utils_conversion.json_file_to_namedtuple(config)

# Set of main folders.
_FOLDERS = {}

# Set of sub-folders.
_SUB_FOLDERS = {
    "raw",
    "raw_error",
    "parsed",
    "parsed_error",
    "organized",
}



def init():
    """Initializes in readiness for io.

    """
    processed = []
    for project in config.projects:
        for feed in project.feeds:
            if feed.source not in processed:
                for sub_folder in _SUB_FOLDERS:
                        folder = _DOCS_FOLDER
                        for name in (project.name, feed.source, sub_folder):
                            folder = os.path.join(folder, name)
                            if not os.path.exists(folder):
                                os.makedirs(folder)
                processed.append(feed.source)


def get_folder(project, source, sub_folder):
    """Returns a project folder pointer in readiness for io.

    :param str project: Name of a supported project.
    :param str source: Name of a document source (e.g. esdoc-q).
    :param str sub_folder: Name of a sub-folder.

    :rtype: str

    """
    folder = _DOCS_FOLDER
    for name in (project, source, sub_folder):
        folder = os.path.join(folder, name)

    return folder


def reset_sub_folder(sub_folder):
    """Removes all files froma sub-folder.

    :param str sub_folder: Sub folder to be cleared.

    """
    processed = []
    for project in config.projects:
        for feed in project.feeds:
            if feed.source not in processed:
                folder = _DOCS_FOLDER
                for name in (project.name, feed.source, sub_folder):
                    folder = os.path.join(folder, name)
                shutil.rmtree(folder)
                os.makedirs(folder)
                processed.append(feed.source)


def get_documents(sub_folder):
    """Yields documents for processing.

    :param str sub_folder: Sub folder to be processed.

    :rtype: generator

    """
    processed = []
    for project, feeds in ((p.name, p.feeds) for p in config.projects):
        for source in (f.source for f in feeds):
            folder = get_folder(project, source, sub_folder)
            if folder not in processed:
                for fpath in glob.iglob(os.path.join(folder, "*.*")):
                    yield project, source, fpath
                processed.append(folder)


def get_count(sub_folder):
    """Returns subfolder document count.

    :param str sub_folder: A document sub-folder.

    :rtype: int

    """
    processed = []
    count = 0
    for project, feeds in ((p.name, p.feeds) for p in config.projects):
        for source in (f.source for f in feeds):
            folder = get_folder(project, source, sub_folder)
            if folder not in processed:
                count = count + sum(glob.iglob(os.path.join(folder, "*.*")))

    return count