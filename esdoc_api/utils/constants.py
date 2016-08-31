# -*- coding: utf-8 -*-
"""
.. module:: constants.py
   :platform: Unix
   :synopsis: Constants used across web-service.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.data import get_data



# HTTP CORS header.
HTTP_HEADER_Access_Control_Allow_Origin = "Access-Control-Allow-Origin"

# Default endpoint.
DEFAULT_ENDPOINT = r'/2/ops/heartbeat'

# Token used to indicate that all document types are in scope.
DOCUMENT_TYPE_ALL = '*'

# Set of document types loaded from file system.
DOCUMENT_TYPES = get_data('document_types')

# Map of document types to keys.
MAPPED_DOCUMENT_TYPES = {i['key'].upper(): i for i in DOCUMENT_TYPES}

# Document version related constants.
DOCUMENT_VERSION_ALL = '*'
DOCUMENT_VERSION_LATEST = 'latest'
DOCUMENT_VERSIONS = [
    DOCUMENT_VERSION_ALL,
    DOCUMENT_VERSION_LATEST
    ]

# Set of projects loaded from file system.
PROJECT = get_data('projects')

# Set of sub-projects loaded from file system.
SUB_PROJECT = get_data('sub_projects')

# Set of document versions loaded from file system.
DOCUMENT_VERSION = get_data('document_versions')

