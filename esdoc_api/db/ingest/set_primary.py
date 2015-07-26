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
    instance.Institute_ID = cache.get_institute_id(ctx.doc.meta.institute)
    instance.Name = unicode(ctx.doc.ext.display_name)
    instance.Project_ID = cache.get_project_id(ctx.doc.meta.project)
    instance.Source_Key = unicode(ctx.doc.meta.source_key)
    instance.Type = unicode(ctx.doc.meta.type)
    instance.UID = unicode(ctx.doc.meta.id)
    instance.Version = ctx.doc.meta.version

    # Persist.
    try:
        session.insert(instance)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        raise StopIteration("Document already ingested")
    else:
        ctx.primary = instance

