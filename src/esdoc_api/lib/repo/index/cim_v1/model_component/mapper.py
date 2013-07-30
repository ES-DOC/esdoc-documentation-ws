"""
.. module:: esdoc_api.lib.repo.index.cim_v1.model_component.mapper.py
   :platform: Unix, Windows
   :synopsis: Maps facets derived from parse over a cim.v1.software.model_component document.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from esdoc_api.lib.repo.index.cim_v1.model_component.parser import parse
from esdoc_api.lib.repo.index.cim_v1.model_component.reducer import reduce
from esdoc_api.lib.utils.convertors import convert_to_spaced_case
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


# Set of component display name mappings.
_COMPONENT_DISPLAY_NAMES = {
    'Aerosol Emission And Conc' : 'Emission And Concentration',
    'Aerosol Model' :  'Model',
    'Aerosol Transport' :  'Transport',
    'Atmos Convect Turbul Cloud' : 'Convection Cloud Turbulence',
    'Atmos Cloud Scheme' : 'Cloud Scheme',
    'Atmos Dynamical Core' : 'Dynamical Core',
    'Atmos Advection' : 'Advection',
    'Atmos Orography And Waves' : 'Orography And Waves',
    'Atmos Radiation' : 'Radiation',
    'Atm Chem Transport' : 'Transport',
    'Atm Chem Photo Chemistry' : 'Photo Chemistry',
    'Atm Chem Heterogen Chemistry' : 'Heterogen Chemistry',
    'Atm Chem Gas Phase Chemistry' : 'Gas Phase Chemistry',
    'Atm Chem Emission And Conc' : 'Emission And Conc',
    'Land Ice Glaciers' : 'Glaciers',
    'Land Ice Sheet' : 'Sheet',
    'Land Ice Shelves' : 'Shelves',
    'Land Ice Shelves Dynamics' : 'Dynamics',
    'Land Surface Albedo' : 'Albedo',
    'Land Surface Carbon Cycle' : 'Carbon Cycle',
    'Land Surface Energy Balance' : 'Energy Balance',
    'Land Surface Lakes' : 'Lakes',
    'Land Surface Snow' : 'Snow',
    'Land Surface Soil' : 'Soil',
    'Land Surface Vegetation' : 'Vegetation',
    'Land Surf Soil Heat Treatment' : 'Heat Treatment',
    'Land Surf Soil Hydrology' : 'Hydrology',
    'Ocean Bio Boundary Forcing' : 'Boundary Forcing',
    'Ocean Bio Chemistry' : 'Chemistry',
    'Ocean Bio Gas Exchange' : 'Gas Exchange',
    'Ocean Bio Tracers' : 'Tracers',
    'Ocean Bio Tracers Ecosystem' : 'Ecosystem',
    'Ocean Advection' : 'Advection',
    'Ocean Boundary Forcing' : 'Boundary Forcing',
    'Ocean Bound Forcing Tracers' : 'Tracers',
    'Ocean Interior Mixing' : 'Interior Mixing',
    'Ocean Lateral Physics' : 'Lateral Physics',
    'Ocean Lateral Phys Momentum' : 'Momentum',
    'Ocean Lateral Phys Tracers' : 'Tracers',
    'Ocean Mixed Layer' : 'Mixed Layer',
    'Ocean Up And Low Boundaries' : 'Up And Low Boundaries',
    'Ocean Vertical Physics' : 'Vertical Physics',
    'Sea Ice Dynamics' : 'Dynamics',
    'Sea Ice Thermodynamics' : 'Thermodynamics'
}


def map(m):
    """Maps a cim v1 model component object instance to a set of facets.

    :param m: A model component.
    :type m: pyesdoc.ontologies.cim.v1.software.ModelComponent

    """
    _map(reduce(parse(m)))


def _get_facet_type(type_id):
    """Returns a facet type from loacl cache.

    :param type: Facet type identifier.
    :type type: int

    """
    if _State.facet_types is None:
        _State.load()
        
    return _State.facet_types[type_id]


def _get_facet_relation_type(type_id):
    """Returns a facet relation type from loacl cache.

    :param type: Facet relation type identifier.
    :type type: int

    """
    if _State.facet_relation_types is None:
        _State.load()

    return _State.facet_relation_types[type_id]


def _get_facet(type_id, key, value, value_for_display=None, key_for_sort=None):
    """Returns a facet (creating it if necessary).

    :param type: Facet type identifier.
    :type type: int

    :param key: Facet key.
    :type key: str

    :param value: Facet value.
    :type value: str
    
    :param value_for_display: Facet display value.
    :type value_for_display: str

    :param key_for_sort: Facet sort key.
    :type key_for_sort: str

    :returns: A facet instance.
    :rtype: esdoc_api.models.Facet

    """
    return utils.create_facet(_get_facet_type(type_id),
                              key,
                              value,
                              value_for_display=value_for_display,
                              key_for_sort=key_for_sort)


def _set_facet_relation(type_id, from_facet, to_facet):
    """Creates a facet relation (if necessary).

    :param type_id: Facet relation type identifier.
    :type type_id: int

    :param from_facet: From facet.
    :type from_facet: esdoc_api.models.Facet
    
    :param to_facet: To facet.
    :type to_facet: esdoc_api.models.Facet

    """
    utils.create_facet_relation(_get_facet_relation_type(type_id), from_facet, to_facet)


def _get_model_facet_set(m):
    """Returns set of model facets.

    :param m: A model component.
    :type m: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: Set of model facets.
    :rtype: tuple

    """
    return _get_facet(models.ID_OF_FACET_MODEL,
                      _get_model_facet_key(m),
                      _get_model_facet_value(m))


def _get_model_facet_key(m):
    """Returns a model facet key.

    :param m: A model component.
    :type m: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: Key to be assigned to the model facet.
    :rtype: str

    """
    return "".join(m.short_name.upper())


def _get_model_facet_value(m):
    """Returns a model facet value.

    :param m: A model component.
    :type m: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: Value to be assigned to the model facet.
    :rtype: str

    """
    return m.short_name.upper()


def _get_component_facet_set(c):
    """Returns set of component facets.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: Set of component facets.
    :rtype: tuple

    """
    return _get_facet(models.ID_OF_FACET_COMPONENT,
                      _get_component_facet_key(c),
                      _get_component_facet_value(c),
                      value_for_display = _get_component_facet_display_value(c)), \
           _get_facet(models.ID_OF_FACET_COMPONENT,
                      _get_component_facet_key(c.parent),
                      _get_component_facet_value(c.parent)) if c.parent is not None else None


def _get_component_facet_key(c):
    """Returns a component facet key.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: Key to be assigned to the component facet.
    :rtype: str

    """
    key = ""
    if c.parent is not None:
        key += _get_component_facet_key(c.parent)
        key += '.'
    key += "".join(c.type.upper().split())
    return key


def _get_component_facet_value(c):
    """Returns a component facet value.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: Value to be assigned to the component facet.
    :rtype: str

    """
    return convert_to_spaced_case(c.type)


def _get_component_facet_display_value(c):
    """Returns a component facet display value.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: Display value to be assigned to the component facet.
    :rtype: str

    """
    value = convert_to_spaced_case(c.type)
    return None if value not in _COMPONENT_DISPLAY_NAMES else _COMPONENT_DISPLAY_NAMES[value]


def _set_component_facet_relations(mf, cf, pcf):
    """Assigns relationships between a component facet and other facets.

    :param mf: A model facet.
    :type mf: esdoc_api.models.Facet

    :param cf: A component facet.
    :type cf: esdoc_api.models.Facet

    :param cf: A parent component facet.
    :type cf: esdoc_api.models.Facet

    """
    _set_facet_relation(models.ID_OF_FACET_RELATION_FROM_MODEL_2_COMPONENT, mf, cf)
    if pcf is not None:
        _set_facet_relation(models.ID_OF_FACET_RELATION_FROM_COMPONENT_2_COMPONENT, pcf, cf)


def _get_property_facet_set(p):
    """Returns set of component property facets.

    :param p: A component property.
    :type p: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    :returns: Set of component property facets.
    :rtype: tuple

    """
    return _get_facet(models.ID_OF_FACET_PROPERTY,
                      _get_property_facet_key(p, True),
                      _get_property_facet_value(p),
                      value_for_display = _get_property_facet_display_value(p),
                      key_for_sort = _get_property_facet_sort_key(p)), \
           _get_facet(models.ID_OF_FACET_PROPERTY,
                      _get_property_facet_key(p.parent, True),
                      _get_property_facet_value(p.parent)) if p.parent is not None else None


def _get_property_facet_key(p, include_component_key):
    """Returns a component property facet key.

    :param p: A component property.
    :type p: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    :param include_component_key: Flag indicating whether component key is to be pre-prended.
    :type include_component_key: bool
    
    :returns: Key to be assigned to the component property facet.
    :rtype: str

    """
    key = ""
    if include_component_key:
        key = _get_component_facet_key(p.component)
        key += '>'
    if p.parent is not None:
        key += _get_property_facet_key(p.parent, False)
        key += '.'
    key += p.short_name.upper()
    return "".join(key.split())


def _get_property_facet_sort_key(p):
    """Returns a component property facet sort key.

    :param p: A component property.
    :type p: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    :returns: Sort key to be assigned to the component property facet.
    :rtype: str

    """
    # Set of overrides.
    overrides = {
        "CORE PROPERTIES" : "AAA"
    }

    # Return override when appropriate.
    key = None
    if p.short_name.upper() in overrides:
        key = overrides[p.short_name.upper()]
    return key


def _get_property_facet_value(p):
    """Returns a component property facet value.

    :param p: A component property.
    :type p: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    :returns: Value to be assigned to the component property facet.
    :rtype: str

    """
    return convert_to_spaced_case(p.short_name)


def _get_property_facet_display_value(p):
    """Returns a component property facet display value.

    :param p: A component property.
    :type p: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    :returns: Display value to be assigned to the component property facet.
    :rtype: str

    """
    # Remove key properties prefixes.
    value = convert_to_spaced_case(p.short_name)
    if value.find("Key Properties") != -1:
        return "Key Properties"
    else:
        return None


def _set_property_facet_relations(mf, cf, pf, ppf):
    """Assigns relationships between a component property facet and other facets.

    :param mf: A model facet.
    :type mf: esdoc_api.models.Facet

    :param cf: A component facet.
    :type cf: esdoc_api.models.Facet

    :param pf: A component property facet.
    :type pf: esdoc_api.models.Facet

    :param ppf: A parent component property facet.
    :type ppf: esdoc_api.models.Facet

    """
    _set_facet_relation(models.ID_OF_FACET_RELATION_FROM_MODEL_2_PROPERTY, mf, pf)
    _set_facet_relation(models.ID_OF_FACET_RELATION_FROM_COMPONENT_2_PROPERTY, cf, pf)
    if ppf is not None:
        _set_facet_relation(models.ID_OF_FACET_RELATION_FROM_PROPERTY_2_PROPERTY, ppf, pf)


def _get_value_facet_set(v):
    """Returns set of component property value facets.

    :param v: A component property value.
    :type v: str

    :returns: Set of component property value facets.
    :rtype: tuple

    """
    return _get_facet(models.ID_OF_FACET_VALUE,
                      _get_value_facet_key(v),
                      _get_value_facet_value(v))


def _get_value_facet_key(v):
    """Returns a component property value facet key.

    :param v: A component property value.
    :type v: str

    :returns: Key to be assigned to the component property value facet.
    :rtype: str

    """
    return "".join(v.upper().split())


def _get_value_facet_value(v):
    """Returns a component property value facet value.

    :param v: A component property value.
    :type v: str

    :returns: Value to be assigned to the component property value facet.
    :rtype: str

    """
    return v


def _set_value_facet_relations(mf, pf, vf):
    """Assigns relationships between a component property value facet and other facets.

    :param mf: A model facet.
    :type mf: esdoc_api.models.Facet

    :param pf: A component property facet.
    :type pf: esdoc_api.models.Facet

    :param vf: A component property value facet.
    :type vf: esdoc_api.models.Facet

    """
    _set_facet_relation(models.ID_OF_FACET_RELATION_FROM_PROPERTY_2_VALUE, pf, vf)
    _set_facet_relation(models.ID_OF_FACET_RELATION_FROM_MODEL_2_VALUE, mf, vf)


def _map(m_reduced):
    """Maps a reduced model component to a set of facets.

    :param m_reduced: Model after being reduced.
    :type m_reduced: tuple

    """
    # Model name.
    m, c_list = m_reduced
    mf = _get_model_facet_set(m)

    # Components.
    for c, p_list in c_list:
        cf, pcf = _get_component_facet_set(c)
        _set_component_facet_relations(mf, cf, pcf)

        # Component properties.
        for p, v_list in p_list:
            pf, ppf = _get_property_facet_set(p)
            _set_property_facet_relations(mf, cf, pf, ppf)

            # Component property values.
            for v in v_list:
                vf = _get_value_facet_set(v)
                _set_value_facet_relations(mf, pf, vf)
                