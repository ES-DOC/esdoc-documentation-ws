"""
.. module:: esdoc_api.lib.db.facets.cim_v1.numerical_experiment.mapper.py
   :platform: Unix, Windows
   :synopsis: Maps facets derived from parse over a cim.v1.software.numerical_experiment document.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.lib.db.facets.utils import get_facet
from esdoc_api.lib.db.facets.utils import set_facet_relation
from esdoc_api.models.entities.facet_relation_type import *
from esdoc_api.models.entities.facet_type import *



# Set of facet types.
_facet_types = get_facet_types()


# Set of facet relation types.
_facet_relation_types = get_facet_relation_types()


def map(e):
    """Maps a cim v1 numerical experiment object instance to a set of facets.

    :param e: A numerical experiment document.
    :type e: pycim.v1.activity.NumericalExperiment

    """
    _map(_reduce(e))


def _reduce(e):
    """Performs a reduce (fold) over a model in readiness for later processing.

    :param e: A numerical experiment document.
    :type e: pycim.v1.activity.NumericalExperiment

    :returns: A numerical experiment document.
    :rtype: pycim.v1.activity.NumericalExperiment

    """
    return e


def _get_facet(type_id, key, value):
    """Returns a facet (creating it if necessary).

    :param type: Facet type identifier.
    :param key: Facet key.
    :param value: Facet value.
    :type type: int
    :type key: str
    :type value: str

    :returns: A facet instance.
    :rtype: esdoc_api.models.entities.entity.Facet

    """
    return get_facet(_facet_types[type_id], key, value)


def _set_facet_relation(type, from_facet, to_facet):
    """Creates a facet relation (if necessary).

    :param type: Facet relation type identifier.
    :param from_facet: From facet.
    :param to_facet: To facet.
    :type type: int
    :type from_facet: esdoc_api.models.entities.entity.Facet
    :type to_facet: esdoc_api.models.entities.entity.Facet

    """
    set_facet_relation(_facet_relation_types[type], from_facet, to_facet)


def _map(e_reduced):
    """Maps a reduced numerical experiment to a set of facets.

    :param e_reduced: A reduced numerical experiment document.
    :type e_reduced: pycim.v1.activity.NumericalExperiment

    """
    def get_key_of_experiment_facet(e):
        return e.short_name.upper()


    def get_value_of_experiment_facet(e):
        return e.short_name


    def get_experiment_facets(e):
        return _get_facet(ID_OF_FACET_EXPERIMENT,
                          get_key_of_experiment_facet(e),
                          get_value_of_experiment_facet(e))

    # Experiment name.
    e = e_reduced
    ef = get_experiment_facets(e)
                