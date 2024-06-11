# -*- coding: utf-8 -*-
"""
.. module:: core.py
   :platform: Unix
   :synopsis: Set of core repo data access operations.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import inspect

import sqlalchemy as sa

from esdoc_api.db import session



def text_filter(qry, field, key):
    """Applies a text based filter expression.

    """
    return qry.filter(sa.func.upper(field) == str(key).strip().upper())


def like_filter(qry, field, expression):
    """Applies a like based filter expression.

    """
    return qry.filter(field.like('%' + expression + '%'))


def sort(etype, collection):
    """Sorts collection via type sort key.

    :param class etype: A supported entity type.
    :param list collection: Collection of entities.

    :returns: Sorted collection.
    :rtype: list

    """
    return [] if collection is None else etype.get_sorted(collection)


def get_all(etype):
    """Gets all instances of the entity.

    :param class etype: A supported entity type.

    :returns: Entity collection.
    :rtype: list

    """
    return get_by_facet(etype, None, get_iterable=True)


def get_by_facet(
    etype,
    efilter,
    order_by=None,
    get_iterable=False
    ):
    """Gets entity instance by facet.

    :param class etype: A supported entity type.
    :param expression efilter: Entity filter expression.
    :param expression order_by: Sort expression.
    :param bool get_iterable: Flag indicating whether to return an iterable or not.

    :returns: Entity or entity collection.
    :rtype: Sub-class of db.models.Entity

    """
    qry = session.query(etype)
    if efilter is not None:
        if inspect.isfunction(efilter):
            efilter(qry)
        else:
            qry = qry.filter(efilter)
    if order_by is not None:
        if inspect.isfunction(order_by):
            order_by(qry)
        else:
            qry = qry.order_by(order_by)

    # Return accordingly.
    # ... first
    if not get_iterable:
        return qry.first()
    # ... sorted collection
    elif order_by is None:
        return sort(etype, qry.all())
    # ... ordered collection
    else:
        return qry.all()


def insert(target):
    """Marks target instance(s) for insertion.

    :param target: Target instance(s) for insertion.
    :type target: Sub-class of db.models.Entity or list

    """
    try:
        iter(target)
    except TypeError:
        target = [target]

    for target in target:
        session.insert(target)


def delete(target):
    """Marks target instance(s) for deletion.

    :param target: Target instance(s) for deletion.
    :type target: Sub-class of db.models.Entity or list

    """
    try:
        iter(target)
    except TypeError:
        target = [target]

    for target in target:
        session.delete(target)


def delete_by_type(etype, callback=None):
    """Deletes all entities of passed type.

    :param class etype: A supported entity type.
    :param function callback: Pointer to a function that will perform callback.

    """
    if callback is None:
        delete_by_facet(etype, etype.id > 0)
    else:
        for instance in get_all(etype):
            callback(instance.id)


def delete_by_facet(etype, efilter):
    """Delete entity instance by id.

    :param class etype: A supported entity type.
    :param expression|func efilter: Filter to apply.

    """
    qry = session.query(etype)
    if inspect.isfunction(efilter):
        efilter(qry)
    else:
        qry = qry.filter(efilter)
    qry.delete()


def delete_by_id(etype, eid):
    """Delete entity instance by id.

    :param class type: A supported entity type.
    :param int eid: ID of entity.

    """
    delete_by_facet(etype, etype.id == eid)


def delete_by_name(etype, name):
    """Deletes an entity instance by it's name.

    :param class etype: A supported entity type.
    :param str name: Name of entity.

    """
    delete_by_facet(etype, etype.name == name)
