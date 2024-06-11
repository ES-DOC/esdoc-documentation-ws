# -*- coding: utf-8 -*-
"""
.. module:: set_external_id.py
   :platform: Unix
   :synopsis: Sets document DRS index.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy

from esdoc_api.db import models, session



def execute(ctx):
    """Creates document index.

    :param object ctx: Document processing context information.

    """
    # Escape if there are no DRS keys defined.
    if not ctx.doc.meta.drs_path:
        return

    # Instantiate.
    idx = models.DocumentDRS()
    idx.document_id = ctx.primary.id
    idx.path = str(ctx.doc.meta.drs_path)
    idx.project = ctx.primary.project

    # Set keys.
    for index, key in enumerate(ctx.doc.meta.drs_keys):
        if index > 7:
            break
        elif key is not None:
            key = str(key).upper()
            setattr(idx, "key_0" + str(index + 1), key)

    # Insert.
    try:
        session.insert(idx)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
