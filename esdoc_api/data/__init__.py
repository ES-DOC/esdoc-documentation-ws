# -*- coding: utf-8 -*-
"""
.. module:: data.__init__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Data sub-package initialization file.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import os

from esdoc_api.utils import convert



def get_data(typeof):
	"""Loads a data file from the file system.

	"""
	fpath = os.path.join(os.path.dirname(__file__), typeof)
	fpath = "{}.json".format(fpath)
	data = convert.json_file_to_dict(fpath, convert.str_to_underscore_case)

	return data[convert.str_to_camel_case(typeof)]
