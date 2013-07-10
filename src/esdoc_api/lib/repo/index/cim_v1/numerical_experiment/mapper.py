"""
.. module:: esdoc_api.lib.repo.index.cim_v1.numerical_experiment.mapper.py
   :platform: Unix, Windows
   :synopsis: Maps facets derived from parse over a cim.v1.software.numerical_experiment document.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.models as models
import esdoc_api.lib.repo.utils as utils



# Set of facet types.
_facet_types = dao.get_facet_types()

# Set of facet relation types.
_facet_relation_types = dao.get_facet_relation_types()


def map(e):
    """Maps a cim v1 numerical experiment object instance to a set of facets.

    :param e: A numerical experiment document.
    :type e: pyesdoc.ontologies.cim.v1.activity.NumericalExperiment

    """
    _map(_reduce(e))


def _reduce(e):
    """Performs a reduce (fold) over a model in readiness for later processing.

    :param e: A numerical experiment document.
    :type e: pyesdoc.ontologies.cim.v1.activity.NumericalExperiment

    :returns: A numerical experiment document.
    :rtype: pyesdoc.ontologies.cim.v1.activity.NumericalExperiment

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
    :rtype: esdoc_api.lib.repo.models.Facet

    """
    return utils.create_facet(_facet_types[type_id], key, value)


def _set_facet_relation(type, from_facet, to_facet):
    """Creates a facet relation (if necessary).

    :param type: Facet relation type identifier.
    :param from_facet: From facet.
    :param to_facet: To facet.
    :type type: int
    :type from_facet: esdoc_api.lib.repo.models.Facet
    :type to_facet: esdoc_api.lib.repo.models.Facet

    """
    utils.create_facet_relation(_facet_relation_types[type], from_facet, to_facet)


def _map(e_reduced):
    """Maps a reduced numerical experiment to a set of facets.

    :param e_reduced: A reduced numerical experiment document.
    :type e_reduced: pyesdoc.ontologies.cim.v1.activity.NumericalExperiment

    """
    def get_key_of_experiment_facet(e):
        return e.short_name.upper()


    def get_value_of_experiment_facet(e):
        return e.short_name


    def get_experiment_facets(e):
        return _get_facet(models.ID_OF_FACET_EXPERIMENT,
                          get_key_of_experiment_facet(e),
                          get_value_of_experiment_facet(e))

    # Experiment name.
    e = e_reduced
    ef = get_experiment_facets(e)
                