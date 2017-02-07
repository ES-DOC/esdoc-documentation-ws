# -*- coding: utf-8 -*-
"""

.. module:: schemas.extender.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC Errata - endpoint validation schema cache extender.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

import pyesdoc

from esdoc_api.utils import constants


# Schema extender functions mapped by schema type and endpoint.
_EXTENDERS = collections.defaultdict(dict)


def extend(schema, typeof, endpoint):
	"""Extends a JSON schema with data pulled from controlled vocabularies.

	:param dict schema: A JSON schema being extended.
	:param str typeof: Type of JSON schema to be extended.
	:param str endpoint: Endpoint being mapped to a JSON schema.

	"""
	try:
		extender = _EXTENDERS[endpoint][typeof]
	except KeyError:
		pass
	else:
		extender(schema)


def _2_document_retrieve_params(schema):
	"""Extends a JSON schema used to validate an HTTP operatino.

	"""
	schema['properties']['encoding']['items']['enum'] = \
		list(pyesdoc.constants.ENCODINGS_ALL)


def _2_summary_search_params(schema):
	"""Extends a JSON schema used to validate an HTTP operatino.

	"""
	print "TODO: ensure document type enum validation is case insenstive"
	schema['properties']['document_type']['items']['enum'] = \
		[i['key'] for i in constants.DOCUMENT_TYPES]
	schema['properties']['document_version']['items']['enum'] = \
		list(constants.DOCUMENT_VERSIONS)


# Map endpoints to extenders.
_EXTENDERS['/2/document/retrieve']['params'] = _2_document_retrieve_params
_EXTENDERS['/2/summary/search']['params'] = _2_summary_search_params
