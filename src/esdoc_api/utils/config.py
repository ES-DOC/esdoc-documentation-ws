# -*- coding: utf-8 -*-

"""
.. module:: utils.config.py
   :copyright: Copyright "Feb 7, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Configuration utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import os

from .convert import json_file_to_namedtuple



# Module exports.
__all__ = [
    'api',
    'core',
    'db',
    'initialize'
]



# API configuration data.
api = None

# Core configuration data.
core = None

# DB configuration data.
db = None


# Config filename.
_CONFIG_FILENAME = 'config.json'


def _get_config_filepath():
    """Returns configuration file path."""
    fpath = os.path.dirname(__file__)
    fpath = os.path.dirname(fpath)
    fpath = os.path.join(fpath, _CONFIG_FILENAME)
    if not os.path.exists(fpath):
        msg = "Configuration file does not exist :: {0}".format(fpath)
        raise RuntimeError(msg)

    return fpath


def initialize():
    """Initializes configuration."""
    # Escape if already initialized.
    if api is not None:
        return

    global api
    global core
    global db

    # Cache config section pointers.
    data = json_file_to_namedtuple(_get_config_filepath())
    api = data.api
    core = data.core
    db = data.db


# Auto-initialize.
initialize()