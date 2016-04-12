# -*- coding: utf-8 -*-
"""
.. module:: set_primary.py
   :platform: Unix
   :synopsis: Sets document primary index.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy

from esdoc_api.db import cache, models, session



def execute(ctx):
    """Creates document index.

    :param object ctx: Document processing context information.

    """
    # Instantiate.
    instance = models.Document()
    instance.institute = ctx.doc.meta.institute
    instance.name = unicode(ctx.doc.ext.display_name)
    instance.project = ctx.doc.meta.project.strip().lower()
    instance.source = unicode(ctx.doc.meta.source_key)
    instance.type = unicode(ctx.doc.meta.type)
    instance.uid = unicode(ctx.doc.meta.id)
    instance.version = ctx.doc.meta.version

    # Persist.
    try:
        session.insert(instance)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        raise StopIteration("Document already ingested")
    else:
        ctx.primary = instance

