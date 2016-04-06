# -*- coding: utf-8 -*-
"""
.. module:: undo.py
   :platform: Unix
   :synopsis: Undoes document ingestion.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import dao



def main(uid, version):
	"""Executes the uningest process for a single document.

    :param str|uuid.UUID uid: Document unique identifier.
    :param str|int version: Document version.

	"""
	doc = dao.get_document(uid, version)
	if doc:
		dao.delete_document(doc.id)
