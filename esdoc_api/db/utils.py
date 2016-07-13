# -*- coding: utf-8 -*-
"""
.. module:: db.utils.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Database utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy

import pyesdoc

from esdoc_api.db import dao
from esdoc_api.db import models
from esdoc_api.db import session
from esdoc_api.utils import logger



def create_node(type_of, field, project='cmip5', sort_text=None):
    """Creates a facet node (if necessary).

    :param str project: Project with which facet node is associated.
    :param str type_of: Facet node type.
    :param str field: Facet node field.
    :param str sort_text: Text used in sort scenarios.

    :returns: A facet node.
    :rtype: models.Node

    """
    def get_field_id(fld):
        """Parses a field representation and returns the field id."""
        if isinstance(fld, models.Node):
            return u'n' + unicode(fld.id)
        elif isinstance(fld, models.NodeField):
            return unicode(fld.id)
        else:
            return unicode(fld)

    # Parse field.
    if isinstance(field, (models.Node, models.NodeField)):
        field = get_field_id(field)
    elif isinstance(field, (str, unicode)):
        field = get_field_id(create_node_field(field))
    elif isinstance(field, tuple):
        field = u",".join([get_field_id(f) for f in field])
    else:
        raise ValueError("Node field cannot be parsed:: {0} :: {1}".format(type(field), field))

    # Create node.
    node = models.Node()
    node.project = project
    node.type_of = type_of
    node.field = field

    # Insert.
    try:
        session.insert(node)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        node = dao.get_node(project, type_of, field)
    else:
        logger.log("INDEXING :: CORE :: created node {0}".format(node))

    # Set sort value (if necessary).
    if sort_text is not None:
        field = unicode(create_node_field(sort_text).id)
        if node.sort_field != field:
            node.sort_field = field
            session.commit()

    return node


def create_node_field(text):
    # Create.
    field = models.NodeField()
    field.text = text

    # Insert.
    try:
        session.insert(field)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        field = dao.get_node_field(text)
    else:
        logger.log("INDEXING :: CORE :: created field {0}".format(field))

    return field


def create_node_combination(type_of, nodeset, project='cmip5'):
    """Creates a node combination (if necessary).

    :param str type_of: Facet combination type.
    :param str nodeset: Set of nodes acting as a vector.
    :param str project: Project with which a facet combination is associated.

    :returns: A facet node combination.
    :rtype: models.NodeCombination

    """
    # Set vector.
    vector = u""
    for index, node in enumerate(nodeset):
        if index > 0:
            vector += u"-"
        vector += unicode(node.id)

    # Create.
    combo = models.NodeCombination()
    combo.combination = vector
    combo.project = project
    combo.type_of = type_of

    # Insert.
    try:
        session.insert(combo)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        combo = dao.get_node_combination(project, type_of, vector)
    else:
        logger.log("INDEXING :: CORE :: created combination {0}".format(combo))

    return combo


def get_node_value_set(project):
    """Returns set of facet node values filtered by project.

    :param str project: Project with which facet node values are associated.

    :returns: Set of facet node values.
    :rtype: list

    """
    def reduce_value(values, value):
        """The value reducer."""
        return values + [value.id, value.text]

    return reduce(reduce_value, dao.get_node_value_set(project), [])


def get_node_set(project):
    """Returns set of facet nodes filtered by project.

    :param str project: Project with which facet nodes are associated.

    :returns: Set of facet nodes.
    :rtype: list

    """
    def reduce_node(nodes, node):
        """The node reducer."""
        return nodes + [
            node.id,
            models.NODE_TYPES.index(node.type_of),
            node.field
            ]

    return reduce(reduce_node, dao.get_node_set(project), [])


def get_node_field_set(project):
    """Returns set of facet fields filtered by project.

    :param str project: Project with which facet nodes are associated.

    :returns: Set of facet fields.
    :rtype: list

    """
    def reduce_field(fields, field):
        """The node reducer."""
        return fields + [field.id, field.text]

    return reduce(reduce_field, dao.get_node_field_set(project), [])


def get_archived_document(document):
    """Loads a pyesdoc document.

    :param models.Document document: A document.

    :returns: A pyesdoc document.
    :rtype: object

    """
    return pyesdoc.archive.read(document.uid, document.version)
