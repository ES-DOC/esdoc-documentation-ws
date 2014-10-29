# -*- coding: utf-8 -*-
"""
.. module:: cmip5_utils.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP5 external id utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""

def set_cmip5_id(external_id, instance):
    """Helper function to parse a cmip5 external id.

    :param str id: CMIP5 external identifier.
    :param object instance: Parsed external id instance.

    """
    instance.id = external_id.upper()
    instance.drs = instance.id.split('.')
    instance.activity = instance.drs[0]
    instance.project = instance.drs[0]
    instance.product = instance.drs[1]
    instance.institute = instance.drs[2]
    instance.model = instance.drs[3]
    instance.experiment = instance.drs[4]
    instance.frequency = instance.drs[5]
    instance.realm = instance.drs[6]
    instance.mip = instance.drs[7]
    instance.ensemble = instance.drs[8]
    if len(instance.drs) >= 10:
        instance.version = instance.drs[9]
        instance.dataset_id = '.'.join(instance.drs[0:9])
    else:
        instance.version = None
        instance.dataset_id = '.'.join(instance.drs[0:8])

    return instance.drs
