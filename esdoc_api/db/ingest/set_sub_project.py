# -*- coding: utf-8 -*-
"""
.. module:: set_sub_project.py
   :platform: Unix
   :synopsis: Sets document sub-project index.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy

from esdoc_api.db import models
from esdoc_api.db import session



def execute(ctx):
    """Creates document index.

    :param object ctx: Document processing context information.

    """
    # Escape if there are no sub-projects to index.
    if not ctx.doc.meta.sub_projects:
        return

    for sub_project in ctx.doc.meta.sub_projects:
        idx = models.DocumentSubProject()
        idx.project = ctx.doc.meta.project.lower()
        idx.document_id = ctx.primary.id
        idx.sub_project = sub_project.lower()

        # Insert.
        try:
            session.insert(idx)
        except sqlalchemy.exc.IntegrityError:
            session.rollback()
