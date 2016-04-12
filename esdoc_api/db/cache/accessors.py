# -*- coding: utf-8 -*-
"""
.. module:: accessors.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Cache accessor functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import models
from esdoc_api.db.cache import core



def get_doc_encoding(item_id=None):
    """Returns either all document encodings or first document encoding with matching name.

    :param item_id: Document encoding identifier.
    :type item_id: str | int

    :returns: Either a document encoding list or an instance.
    :rtype: list | models.DocumentEncoding

    """
    return core.get(models.DocumentEncoding, item_id)


def get_doc_type(item_id=None):
    """Returns either all document types or first document type with matching name.

    :param item_id: Document type identifier.
    :type item_id: str | int

    :returns: Either a document type list or an instance.
    :rtype: list | models.DocumentType

    """
    return core.get(models.DocumentType, item_id)


