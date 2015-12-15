# -*- coding: utf-8 -*-

"""
.. module:: test_archive.py

   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Executes pyesdoc document archive tests.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
# Module imports.
import nose
import requests

from . import test_utils as tu



def test_search_by_name():
	"""Tests document searching by name."""
	tu.assert_str("XXX", "XXX")
