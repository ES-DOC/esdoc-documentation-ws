# -*- coding: utf-8 -*-
"""
.. module:: indexer.py
   :platform: Unix, Windows
   :synopsis: Indexes a cim.v1.activity.numerical_experiment document.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import models, utils



def index(project, e):
    """Indexes a cim v1 numerical experiment document.

    :param str project: Associated project code.
    :param e: A numerical experiment document.
    :type e: ontologies.cim.v1.activity.NumericalExperiment

    """
    utils.create_node(models.NODE_TYPE_EXPERIMENT, e.short_name, project)
