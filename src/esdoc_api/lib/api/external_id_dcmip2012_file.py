"""
.. module:: esdoc_api.lib.ajax.external_id_dcmip2012_dataset.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates CMIP5 file id handling.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.lib.api.external_id_utils import concat_ds
from esdoc_api.lib.pyesdoc import CIM_1_TYPE_MODEL_COMPONENT
import esdoc_api.lib.repo.dao as dao



def parse(id):
    """Performs a parse over a dcmip-2012 file id.

    :param id: CMIP5 file id.
    :type id: str

    """
    class FileID(object):
        def __init__(self, id):
            id = id.upper()
            self.id = id
            self.drs = id.split('.')
            self.model = self.drs[0]

    return FileID(id)


def do_query(project, id):
    """Query handler for returning documents by dcmip-2012 file id.

    :param project: DCMIP-2012 project identifier.
    :type project: esdoc_api.models.Project

    :param id: DCMIP-2012 file identifier
    :type id: FileID

    :returns: List of found documents.
    :rtype: list

    """
    get = dao.get_document_by_name

    return concat_ds([], get(project.ID, CIM_1_TYPE_MODEL_COMPONENT, id.model))


def is_valid(id):
    """Validates a dcmip-2012 file id.

    :param id: A dcmip-2012 file id.
    :type id: str

    """
    return False if len(id.split('.')) < 1 else True