"""
.. module:: esdoc_api.lib.ajax.external_id_dcmip2012_dataset.py
   :copyright: Copyright "Jul 26, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates CMIP5 file id handling.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""

def is_valid(file_id):
    """Validates a DCMIP-2012 file id.

    :param str file_id: A DCMIP-2012 file id.

    :returns: A flag indicating whether the id is valid or not.
    :rtype: boolean

    """
    if not file_id or not file_id.strip():
        return False
    else:
        return False if len(file_id.strip().split('.')) < 1 else True


def get_parsed(file_id):
    """Returns a parsed a DCMIP-2012 file id.

    :param str file_id: DCMIP-2012 file id.

    :returns: A parsed DCMIP-2012 file id.
    :rtype: object

    """

    class FileID(object):
        def __init__(self):
            self.id = file_id.upper()
            self.drs = self.id.split('.')
            self.model = self.drs[0]

    return FileID(id)


def _yield_doc_by_name_criteria(parsed_id):
    """Yeilds document by name search criteria."""
    yield 'cim.1.software.modelcomponent', parsed_id.model


def do_search(project_id, parsed_id):
    """Executes document search against db.

    :param int project_id: CMIP5 project identifier.
    :param object parsed_id: A parsed CMIP5 dataset identifier

    :returns: A sequence of returned documents.
    :rtype: generator

    """
    for doc_type, doc_name in _yield_doc_by_name_criteria(parsed_id):
        yield dao.get_document_by_name(project_id, doc_type, doc_name)
