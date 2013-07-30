"""
.. module:: esdoc_api.lib.ajax.external_id_utils.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates external id utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

def set_cmip5_id(id, instance):
    """Helper function to parse a cmip5 external id.

    :param id: CMIP5 external identifier.
    :type id: str

    :param instance: Parsed external id instance.
    :type instance: CMIP5DatasetID  | CMIP5FileID

    """
    instance.id = id.upper()
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
    instance.version = instance.drs[9]
    instance.dataset_id = '.'.join(instance.drs[0:9])

    return instance.drs


def concat_ds(document_set, target):
    """Updates document set list.

    :param document_set: A set of documents.
    :type document_set:
    
    :param target: Current document set.
    :type target: list | object

    :returns: Updated document set.
    :rtype: list

    """
    append = True

    if target is None:
        append = False
    elif isinstance(target, list):
        append == True
    else:
        if len(document_set) > 0:
            for i in range(len(document_set)):
                if not isinstance(target, list):
                    if target.ID == document_set[i].ID:
                        append = False
                        break

    if append == True:
        if isinstance(target, list):
            document_set.extend(target)
        else:
            document_set.append(target)

    return document_set
