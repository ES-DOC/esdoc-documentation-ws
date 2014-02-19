"""
.. module:: esdoc_api.lib.repo.index.cim_v1.numerical_experiment.mapper.py
   :platform: Unix, Windows
   :synopsis: Maps facets derived from parse over a cim.v1.software.numerical_experiment document.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.utils as utils



class _State(object):
    """Encpasulates mutable module state.

    """
    facet_types = None
    facet_relation_types = None

    @classmethod
    def load(cls):
        """Loads state into memory.

        """
        # Set of facet types.
        cls.facet_types = dao.get_facet_types()

        # Set of facet relation types.
        cls.facet_relation_types = dao.get_facet_relation_types()


def map(project_id, e):
    """Maps a cim v1 numerical experiment object instance to a set of facets.

    :param int project_id: ID of associated project.

    :param e: A numerical experiment document.
    :type e: pyesdoc.ontologies.cim.v1.activity.NumericalExperiment

    """
    _map(_reduce(e), project_id)


def _reduce(e):
    """Performs a reduce (fold) over a model in readiness for later processing.

    :param e: A numerical experiment document.
    :type e: pyesdoc.ontologies.cim.v1.activity.NumericalExperiment

    :returns: A numerical experiment document.
    :rtype: pyesdoc.ontologies.cim.v1.activity.NumericalExperiment

    """
    return e


def _get_facet_type(type_id):
    """Returns a facet type from local cache."""
    if _State.facet_types is None:
        _State.load()

    return _State.facet_types[type_id]


def _get_facet_relation_type(type_id):
    """Returns a facet relation type from local cache."""
    if _State.facet_relation_types is None:
        _State.load()

    return _State.facet_relation_types[type_id]


def _get_facet(project_id, type_id, key, value, value_for_display=None, key_for_sort=None):
    """Returns a facet (creating it if necessary)."""
    return utils.create_facet(project_id,
                              _get_facet_type(type_id),
                              key,
                              value,
                              value_for_display=value_for_display,
                              key_for_sort=key_for_sort)


def _set_facet_relation(project_id, type_id, from_facet, to_facet):
    """Creates a facet relation (if necessary)."""    
    utils.create_facet_relation(project_id, _get_facet_relation_type(type_id), from_facet, to_facet)


def _map(project_id, e_reduced):
    """Maps a reduced numerical experiment to a set of facets."""
    def get_key_of_experiment_facet(e):
        return e.short_name.upper()


    def get_value_of_experiment_facet(e):
        return e.short_name


    def get_experiment_facets(e):
        return _get_facet(project_id, 
                          models.ID_OF_FACET_EXPERIMENT,
                          get_key_of_experiment_facet(e),
                          get_value_of_experiment_facet(e))

    # Experiment name.
    e = e_reduced
    ef = get_experiment_facets(e)
                