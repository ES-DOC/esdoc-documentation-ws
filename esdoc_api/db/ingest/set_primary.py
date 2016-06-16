# -*- coding: utf-8 -*-
"""
.. module:: set_primary.py
   :platform: Unix
   :synopsis: Sets document primary index.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy

import pyesdoc
from pyesdoc.ontologies import cim
from pyesdoc.utils.convert import str_to_unicode

from esdoc_api.db import models
from esdoc_api.db import session



def parse_cim_1_misc_documentset(instance, doc):
    """Parses a cim.v1.misc.DocumentSet document.

    """
    if doc.model:
        instance.model = unicode(doc.model.short_name)
    if doc.experiment:
        instance.experiment = unicode(doc.experiment.short_name)


# Set of summary field parsers.
_PARSERS = {
    cim.v1.misc.DocumentSet: parse_cim_1_misc_documentset
}


def execute(ctx):
    """Creates document index.

    :param object ctx: Document processing context information.

    """
    # Instantiate.
    instance = models.Document()
    instance.description = str_to_unicode(ctx.doc.ext.description)
    instance.institute = ctx.doc.meta.institute
    instance.language = pyesdoc.DEFAULT_LANGUAGE
    instance.name = unicode(ctx.doc.ext.display_name)
    instance.project = ctx.doc.meta.project.strip().lower()
    instance.source = unicode(ctx.doc.meta.source_key)
    instance.type = unicode(ctx.doc.meta.type)
    instance.uid = unicode(ctx.doc.meta.id)
    instance.version = ctx.doc.meta.version

    # Set summary fields.
    fields = [f for f in ctx.doc.ext.summary_fields if f is not None]
    for index, field in enumerate(fields):
        field = unicode(field)
        if index == 0:
            instance.short_name = field
        elif index == 1:
            instance.long_name = field
        else:
            setattr(instance, 'field_0' + str(index - 1), field)

    # Set other fields.
    try:
        parser = _PARSERS[type(ctx.doc)]
    except KeyError:
        pass
    else:
        parser(instance, ctx.doc)

    # Persist.
    try:
        session.insert(instance)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        raise StopIteration("Document already ingested")
    else:
        ctx.primary = instance

