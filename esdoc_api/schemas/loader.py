# -*- coding: utf-8 -*-
"""

.. module:: schemas.loader.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: ES-DOC Errata - endpoint validation schema cache loader.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import json
import os

from esdoc_api.schemas import extender
from esdoc_api.utils import constants



def load(typeof, endpoint):
	"""Returns a loaded schema.

	"""
	fpath = _get_fpath(typeof, endpoint)
	if os.path.exists(fpath):
		try:
			with open(fpath, 'r') as fstream:
				schema = json.loads(fstream.read())
		except Exception as err:
			print(endpoint, err)
			pass
		else:
			extender.extend(schema, typeof, endpoint)
			return schema


def _get_fpath(typeof, endpoint):
	"""Returns schema file path.

	"""
	endpoint = constants.DEFAULT_ENDPOINT if endpoint == '/' else endpoint
	fname = "{}.json".format(endpoint[1:].replace("/", "."))
	fpath = os.path.join(os.path.dirname(__file__), typeof)

	return os.path.join(fpath, fname)
