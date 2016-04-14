# -*- coding: utf-8 -*-
"""
.. module:: vocab.py
   :platform: Unix
   :synopsis: Data access operations across vocab domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy as sa

import pyesdoc

from esdoc_api.db import session
from esdoc_api.db.models import Document
from esdoc_api.db.models import Institute



def _parse_param(param_val, param_name):
    """Parses an input parameter.

    """
    if param_val is None:
        raise ValueError(param_name)
    param_val = unicode(param_val).strip()
    if not param_val:
        raise ValueError(param_name)
    return param_val


def get_project_institute_counts():
    """Returns institute counts grouped by project.

    :returns: List of counts over a project's institutes.
    :rtype: list

    """
    qry = session.query(sa.func.count(Document.institute),
                        Document.project,
                        Document.institute)
    qry = qry.group_by(Document.project)
    qry = qry.group_by(Document.institute)

    return qry.all()


def create_institute(name, long_name=None, country_code=None, homepage=None):
    """Creates & returns an institute instance.

    :param str name: Institute name.
    :param str long_name: Institute long name.
    :param str country_code: Institute country code.
    :param str homepage: Institute home page.

    :returns: Newly created institute instance.
    :rtype: db.models.Institute

    """
    name = name.upper()
    if not long_name:
        long_name = name
    if not country_code:
        country_code = "--"

    instance = Institute()
    instance.country_code = _parse_param(country_code, 'country_code')
    instance.long_name = _parse_param(long_name, 'long_name')
    instance.name = _parse_param(name, 'name')
    if homepage:
        instance.url = _parse_param(homepage, 'homepage')

    return instance

