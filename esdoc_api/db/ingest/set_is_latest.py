# -*- coding: utf-8 -*-
"""
.. module:: set_is_latest.py
   :platform: Unix
   :synopsis: Sets document is latest index.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import dao
from esdoc_api.db import session
from esdoc_api.utils import constants



def execute(ctx):
    """Creates document index.

    :param object ctx: Document processing context information.

    """
    # Get related documents (sorted by version).
    documents = dao.get_document(ctx.primary.uid,
                                 constants.DOCUMENT_VERSION_ALL,
                                 ctx.primary.project)

    # Uodate flag accordingly.
    for index, document in enumerate(documents):
        document.is_latest = (index == 0)

    # Commit changes.
    session.commit()
