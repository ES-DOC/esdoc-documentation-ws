"""
.. module:: esdoc_api.lib.ajax.external_id_query
   :platform: Unix, Windows
   :synopsis: Encapsulates querying of repository by project specific external document id's.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.models.entities.document import Document
from esdoc_api.lib.utils.xml_utils import CIM_TAG_MODEL_COMPONENT
from esdoc_api.lib.utils.xml_utils import CIM_TAG_NUMERICAL_EXPERIMENT



def _concat(document_set, target):
    """Updates document set set.

    :param document_set: A set of documents.
    :param target: Current document set.
    :type document_set:
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


def cmip5_dataset_id_query(project, id):
    """Query handler for returning documents by cmip5 dataset id.

    :param project: CMIP5 project identifier.
    :param id: CMIP5 dataset identifier
    :type project: esdoc_api.models.entities.Proejct
    :type id: dict

    :returns: List of found documents.
    :rtype: list

    """
    result = []
    
    # Source 1 : From DRS keys.
    get = Document.retrieve_by_drs_keys
    result = _concat(result, get(project,
                                 id.institute,
                                 id.model,
                                 id.experiment,
                                 id.ensemble))

    # Source 2 : From model, experiment (if DRS returned nothing).
    if len(result) == 0:
        get = Document.retrieve_by_name
        result = _concat(result, get(project,
                                     CIM_TAG_MODEL_COMPONENT,
                                     id.model))

        result = _concat(result, get(project,
                                     CIM_TAG_NUMERICAL_EXPERIMENT,
                                     id.experiment))

    # Source 3 : From dataset ID.
    get = Document.retrieve_by_external_id
    return _concat(result, get(project, id.id))
    

def cmip5_file_id_query(project, id):
    """Query handler for returning documents by cmip5 file id.

    :param project: CMIP5 project identifier.
    :param id: CMIP5 file identifier
    :type project: esdoc_api.models.entities.Proejct
    :type id: dict

    :returns: List of found documents.
    :rtype: list

    """
    result = []

    # Source 1 : From DRS keys.
    get = Document.retrieve_by_drs_keys
    result = _concat(result, get(project,
                                 id.institute,
                                 id.model,
                                 id.experiment,
                                 id.ensemble))

    # Source 2 : From model, experiment (if DRS returned nothing).
    if len(result) == 0:
        get = Document.retrieve_by_name
        result = _concat(result, get(project,
                                     CIM_TAG_MODEL_COMPONENT,
                                     id.model))

        result = _concat(result, get(project,
                                     CIM_TAG_NUMERICAL_EXPERIMENT,
                                     id.experiment))    

    # Source 3 : From dataset ID.
    get = Document.retrieve_by_external_id
    return _concat(result, get(project, id.dataset_id))


def cmip5_simulation_id_query(project, id):
    """Query handler for returning documents by cmip5 simulation id.

    :param project: CMIP5 project identifier.
    :param id: CMIP5 simulation identifier
    :type project: esdoc_api.models.entities.Proejct
    :type id: dict

    :returns: List of found documents.
    :rtype: list

    """
    result = []

    # Source 1 : From DRS keys.
    get = Document.retrieve_by_drs_keys
    result = _concat(result, get(project,
                                 id.institute,
                                 id.model,
                                 id.experiment,
                                 id.ensemble,
                                 id.start_year))

    # Source 2 : From model, experiment (if DRS returned nothing).
    if len(result) == 0:
        get = Document.retrieve_by_name
        result = _concat(result, get(project,
                                     CIM_TAG_MODEL_COMPONENT,
                                     id.model))

        result = _concat(result, get(project,
                                     CIM_TAG_NUMERICAL_EXPERIMENT,
                                     id.experiment))    

    # Source 3 : From simulation ID.
    get = Document.retrieve_by_external_id
    return _concat(result, get(project, id.simulation_id))    
                                        

def dcmip2012_dataset_id_query(project, id):
    """Query handler for returning documents by dcmip2012 dataset id.

    :param project: dcmip2012 project identifier.
    :param id: dcmip2012 dataset identifier
    :type project: esdoc_api.models.entities.Proejct
    :type id: dict

    :returns: List of found documents.
    :rtype: list

    """
    get = Document.retrieve_by_name
    return _concat([], get(project, CIM_TAG_MODEL_COMPONENT, id.model))


def dcmip2012_file_id_query(project, id):
    """Query handler for returning documents by dcmip2012 file id.

    :param project: dcmip2012 project identifier.
    :param id: dcmip2012 file identifier
    :type project: esdoc_api.models.entities.Proejct
    :type id: dict

    :returns: List of found documents.
    :rtype: list

    """
    get = Document.retrieve_by_name
    return _concat([], get(project, CIM_TAG_MODEL_COMPONENT, id.model))
