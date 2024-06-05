# -*- coding: utf-8 -*-
"""
.. module:: set_external_id.py
   :platform: Unix
   :synopsis: Sets document external id index.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy

from esdoc_api.db import models
from esdoc_api.db import session



def execute(ctx):
    """Creates document index.

    :param object ctx: Document processing context information.

    """
    # Escape if there is no external id defined.
    if not len(ctx.doc.meta.external_ids):
    	return

    # Pick up first external id.
    external_id = str(ctx.doc.meta.external_ids[0].value).upper()

    # Insert.
    idx = models.DocumentExternalID()
    idx.project = ctx.primary.project
    idx.document_id = ctx.primary.id
    idx.external_id = external_id

    # Insert.
    try:
        session.insert(idx)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
