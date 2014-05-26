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
import os
import shutil

import esdoc_api.pyesdoc.utils.convert as utils_conversion



# Configuration.
config = None

# Set of main folders.
folders = {}

# Set of sub-folders.
sub_folders = {
    "pulled",
    "pulled_error",
    "pulled_accepted",
    "pulled_rejected",
    "ingested",
    "ingested_error",
    "ingested_accepted",
    "ingested_rejected",
    "pushed",
    "pushed_accepted",
    "pushed_error",
    "pushed_rejected",
}

# Set of standard encodings.
ENCODINGS = ['json', 'xml']


def get_sub_folder(project, sub_folder):
    """Initializes & returns a project folder in readiness for io."""
    folder = os.path.dirname(os.path.abspath(__file__))
    for name in ("documents", project, sub_folder):
        folder = os.path.join(folder, name)
        if not os.path.exists(folder):
            os.makedirs(folder)

    return folder


def _init_folders():
    """Initializes folders in readiness for io."""
    # Build dictionaries of project folders.
    for project in config.projects:
        folders[project.name] = {}
        for sub_folder in sub_folders:
            folders[project.name][sub_folder] = \
                get_sub_folder(project.name, sub_folder)


def _init_config():
    """Initializes configuration."""
    global config

    config = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(config, "config.json")
    config = utils_conversion.json_file_to_namedtuple(config)


def init():
    """ Initializes io related objects."""
    _init_config()
    _init_folders()


def reset_sub_folder(sub_folder):
    """Removes all files froma sub-folder.

    :param str sub_folder: Sub folder to be cleared.

    """
    for project in config.projects:
        folder = folders[project.name][sub_folder]
        shutil.rmtree(folder)
        os.makedirs(folder)


def get_documents(doc_type, ctx_class=None):
    """Yields documents for processing.

    :param str doc_type: Type of document being processed.
    :param class ctx_class: Document processing context class.

    :returns: Generator of documents for processing.
    :rtype: generator

    """
    for project, folder in folders[doc_type].items():
        for root, sub_folders, files in os.walk(folder):
            for f in files:
                if ctx_class is None:
                    yield project, f
                else:
                    yield ctx_class(project, os.path.join(root, f))

