# -*- coding: utf-8 -*-

"""
.. module:: test_document_publishing.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes web-service publishing endpoint tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
import os

import requests

import pyesdoc
import pyesdoc.ontologies.cim as cim

from . import test_utils as tu


# Document cache.
_DOCS = []

# Set of target urls.
_URL = os.getenv("ESDOC_API")
_URL_POST = "{}/2/document/create".format(_URL)
_URL_GET = "{}/2/document/retrieve".format(_URL)
_URL_GET_PARAMS = "?encoding={}&id={}&version={}"
_URL_DELETE = "{}/2/document/delete".format(_URL)
_URL_DELETE_PARAMS = "?id={}&version={}"


def _get_test_document():
	"""Returns a test document.

	"""
	doc = pyesdoc.create(
		cim.v2.NumericalExperiment, project="test-project", source="unit-test")
	doc.canonical_name = "anexp"
	doc.name = "an experiment"
	doc.long_name = "yet another experiment"
	doc.rationale = "to state the bleeding obvious"
	doc.meta.id = unicode(doc.meta.id)
	doc.meta.version += 1
	doc.required_period = pyesdoc.create(
		cim.v2.TemporalConstraint, project="test-project", source="unit-test")
	doc.required_period.is_conformance_requested = False
	doc.required_period.meta.id = unicode(doc.required_period.meta.id)
	doc.required_period.name = "too long"

	_DOCS.append(doc)

	return doc


def test_publish():
	"""Tests publishing a document.

	"""
	# Create a document for testing.
	doc = _get_test_document()
	print "doc id =", doc.meta.id

	# Post document to web-service.
	data = pyesdoc.encode(doc, 'json')
	headers = {'Content-Type': 'application/json'}
	response = requests.post(_URL_POST, data=data, headers=headers)

	print response


def test_retrieve():
	"""Tests retrieving a previously published document.

	"""
	pass


def test_republish():
	"""Tests republishing a document.

	"""
	pass


def test_unpublish():
	"""Tests unpublishing a document.

	"""
	pass
