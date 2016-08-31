# -*- coding: utf-8 -*-
"""

.. module:: schemas.cache.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC Errata - endpoint validation schema cache.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

from esdoc_api.schemas import loader



# Cached store of loaded schemas.
_store = collections.defaultdict(dict)



def init(endpoints):
	"""Initializes cache from schemas upon file system.

	:param dict endpoints: Map of application endpoints.

	"""
	for endpoint in endpoints:
		for typeof in {'body', 'params', 'headers'}:
			_store[typeof][endpoint] = loader.load(typeof, endpoint)


def get_schema(typeof, request):
	"""Gets a schema from cache.

	"""
	store = _store[typeof]

	if request.query_arguments:
		print "TODO: resolve schema using query args as well as path", typeof, request.path, request.query_arguments

	return store[request.path]
