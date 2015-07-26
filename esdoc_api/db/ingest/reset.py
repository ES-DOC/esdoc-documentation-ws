# -*- coding: utf-8 -*-
"""
.. module:: resets.py
   :platform: Unix
   :synopsis: Resets document ingestion.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import dao
from esdoc_api.db import session



def execute(ctx):
    """Resets document ingestion.

    :param object ctx: Document processing context information.

    """
    if not ctx.do_reset:
        return

    doc = dao.get_document(ctx.doc.meta.id, ctx.doc.meta.version)
    if doc:
        dao.delete_document(doc.ID)
        session.commit()


