"""
.. module:: handlers_metafor_q.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Exposes Metafor Questionnaire document processing handlers.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.lib.utils.cim_v1 as cim_v1
import esdoc_api.lib.utils.runtime as rt



def _post_set_institute_1(doc):
    """Sets institute derived from contacts."""
    def get_institute(contacts):
        """Returns institute code derived from contact list."""
        for contact in contacts:
            if contact.role == 'centre':
                return contact.abbreviation
        for contact in contacts:
            if contact.role == 'contact' and contact.abbreviation is not None:
                return contact.abbreviation

        return None

    try:
        doc.meta.institute = get_institute(doc.responsible_parties)
    except AttributeError:
        try:
            doc.meta.institute = get_institute(doc.contacts)
        except AttributeError:
            pass


def _post_set_institute_2(doc):
    """Overrides institute code so as to confirm to DRS."""
    if doc.meta.institute is None:
        return

    overrides = {
        'CMA-BCC' : 'BCC',
        'CNRM-GAME' : 'CNRM-CERFACS',
        'GFDL' : 'NOAA-GFDL',
        'GISS' : 'NASA-GISS',
        'NASA GISS' : 'NASA-GISS',
        'NASA' : 'NASA-GISS',
        'NIMR/KMA' : 'NIMR-KMA',
        'STEVE' : 'CSIRO-QCCCE',
    }

    doc.meta.institute = doc.meta.institute.upper()
    if doc.meta.institute in overrides:
        msg = "WARNING :: institute code overidden :: from {0} to {1}"
        msg = msg.format(doc.meta.institute, overrides[doc.meta.institute])
        rt.log(msg)
        doc.meta.institute = overrides[doc.meta.institute]


def _post_set_model_name(doc):
    """Overrides model name so as to confirm to DRS."""
    if doc.type_key != cim_v1.TYPE_KEY_MODEL_COMPONENT:
        return

    overrides = {
        'BCC_CSM1.1' : 'BCC-CSM1.1'
    }

    doc.short_name = doc.short_name.upper()
    if doc.short_name in overrides:
        msg = "WARNING :: model name overidden :: from {0} to {1}"
        msg = msg.format(doc.short_name, overrides[doc.short_name])
        rt.log(msg)
        doc.short_name = overrides[doc.short_name]


# Set of document parsers.
PARSERS = (
    _post_set_institute_1,
    _post_set_institute_2,
    )
