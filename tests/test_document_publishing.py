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

import test_utils as tu


# Cached test document.
_DOC = None

# Set of target urls.
_URL = os.getenv("ESDOC_API")
_URL_POST = "{}/2/document/create".format(_URL)
_URL_PUT = "{}/2/document/update".format(_URL)
_URL_GET = "{}/2/document/retrieve".format(_URL)
_URL_GET_PARAMS = "?encoding={}&id={}&version={}"
_URL_DELETE = "{}/2/document/delete".format(_URL)
_URL_DELETE_PARAMS = "?id={}&version={}"


def _set_test_document():
	"""Returns a test document.

	"""
	global _DOC

	_DOC = pyesdoc.create(
		cim.v2.NumericalExperiment, project="test-project", source="unit-test")
	_DOC.canonical_name = "anexp"
	_DOC.name = "an experiment"
	_DOC.long_name = "yet another experiment"
	_DOC.rationale = "to state the bleeding obvious"
	_DOC.meta.id = unicode(_DOC.meta.id)
	_DOC.meta.version += 1
	_DOC.required_period = pyesdoc.create(
		cim.v2.TemporalConstraint, project="test-project", source="unit-test")
	_DOC.required_period.is_conformance_requested = False
	_DOC.required_period.meta.id = unicode(_DOC.required_period.meta.id)
	_DOC.required_period.name = "too long"

	pyesdoc.extend(_DOC)


def test_publish():
	"""ES-DOC :: WS :: Test publishing a document.

	"""
	# Create a document for testing.
	_set_test_document()

	# Post document to web-service.
	data = pyesdoc.encode(_DOC, 'json')
	headers = {'Content-Type': 'application/json'}
	url = _URL_POST
	response = requests.post(url, data=data, headers=headers)
	assert response.status_code == 200


def _test_retrieve(encoding):
	"""Tests retrieving a specific document encoding."""
	params = _URL_GET_PARAMS.format(encoding, _DOC.meta.id, _DOC.meta.version)
	url = "{}{}".format(_URL_GET, params)
	response = requests.get(url)
	assert response.status_code == 200

	if encoding != 'html':
		doc = pyesdoc.decode(response.text, encoding)
		assert doc.meta.id == _DOC.meta.id
		assert doc.meta.version == _DOC.meta.version
		if pyesdoc.encode(_DOC, encoding) != response.text:
			pass
			# assert pyesdoc.encode(_DOC, encoding) == response.text


def test_retrieve():
	"""ES-DOC :: WS :: Test retrieving a previously published document.

	"""
	for encoding in pyesdoc.ENCODINGS_HTTP:
		tu.init(_test_retrieve, 'retrieval', suffix=encoding)
		yield _test_retrieve, encoding


def test_republish():
	"""ES-DOC :: WS :: Test republishing a document.

	"""
	_DOC.rationale = "to restate the bleeding obvious"
	_DOC.meta.version += 1

	data = pyesdoc.encode(_DOC, 'json')
	headers = {'Content-Type': 'application/json'}
	url = _URL_PUT
	response = requests.put(url, data=data, headers=headers)
	assert response.status_code == 200

	params = _URL_GET_PARAMS.format('json', _DOC.meta.id, _DOC.meta.version)
	url = "{}{}".format(_URL_GET, params)
	response = requests.get(url)
	assert response.status_code == 200

	doc = pyesdoc.decode(response.text, 'json')
	assert doc.meta.id == _DOC.meta.id
	assert doc.meta.version == _DOC.meta.version
	assert doc.rationale == "to restate the bleeding obvious"


def test_unpublish():
	"""ES-DOC :: WS :: Test unpublishing a document.

	"""
	params = _URL_DELETE_PARAMS.format(_DOC.meta.id, _DOC.meta.version)
	url = "{}{}".format(_URL_DELETE, params)
	response = requests.delete(url)
	assert response.status_code == 200

	params = _URL_DELETE_PARAMS.format(_DOC.meta.id, _DOC.meta.version - 1)
	url = "{}{}".format(_URL_DELETE, params)
	response = requests.delete(url)
	assert response.status_code == 200

