"""
.. module:: esdoc_api.lib.repo.index.cim_v1.model_component.parser.py
   :platform: Unix, Windows
   :synopsis: Performs a pre-facet indexing parse over a cim.v1.software.model_component object.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import types

from esdoc_api.lib.pyesdoc.ontologies.cim.v1.types.software.component_property import ComponentProperty



def _set_standard_property(p_tree, values, name, description):
    """Sets & returns a component standard property.

    :param p_tree: A set of component properties.
    :type p_tree: list

    :param values: Property value.
    :type values: str | list

    :param name: Property name.
    :type name: str

    :param description: Property description.
    :type description: str

    :returns: A property.
    :rtype: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    """
    def append_value(p, v):
        if v is not None:
            p.values.append(str(v))

    p = ComponentProperty()
    p.short_name = p.long_name = name
    p.description = description
    if isinstance(values, types.ListType):
        for v in values:
            append_value(p, v)
    else:
        append_value(p, values)
    p_tree.append(p)
    return p


def _set_standard_properties_defaults(c, p_tree):
    """Sets default standard properties.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent
    
    :param p_tree: A set of component properties.
    :type p_tree: list

    """
    _set_standard_property(p_tree,
                           c.description,
                           'Description',
                           'High-level component description')
    _set_standard_property(p_tree,
                           c.short_name,
                           'Short Name',
                           'Abbreviated component name')
    _set_standard_property(p_tree,
                           c.long_name,
                           'Long Name',
                           'Full component name')

                       
def _set_standard_properties_citations(c, p_tree):
    """Sets citation standard properties.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :param p_tree: A set of component properties.
    :type p_tree: list

    """
    def get_citation_title(citation):
        return citation.title.strip()
    
    def get_citation_url(citation):
        if citation.location is None or citation.location.strip() == "":
            return "N/A"
        else:
            return citation.location.strip()

    p = _set_standard_property(p_tree,
                               None,
                               'Citations',
                               'Set of component citations')

    _set_standard_property(p.children,
                           [get_citation_title(i) for i in c.citation_list if i.title is not None],
                           'Title',
                           'Title')
    _set_standard_property(p.children,
                           [get_citation_url(i) for i in c.citation_list if i.title is not None],
                           'Location',
                           'Location')


def _set_standard_properties_pi(c, p_tree):
    """Sets principal investigator standard properties.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :param p_tree: A set of component properties.
    :type p_tree: list

    """
    # Set PI.
    pi = None
    for rp in c.responsible_parties:
        if rp.role and rp.role.upper() == "PI":
            pi = rp
            break
            
    # Set PI properties.
    if pi:
        _set_standard_property(p_tree,
                               pi.individual_name,
                               'PI Name',
                               'PI Name')
        if pi.contact_info:
            _set_standard_property(p_tree,
                                   pi.contact_info.email,
                                   'PI Email Address',
                                   'PI Email Address')


def _set_standard_properties(c):
    """Set component standard properties.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    """
    # Create property group.
    p = _set_standard_property(c.properties,
                               None,
                               'Standard Properties',
                               'Set of properties common to all components')

    # Define sub-property group factories.
    subgroups = [
        _set_standard_properties_defaults,
        _set_standard_properties_pi,
        _set_standard_properties_citations
    ]

    # Create sub-groups.
    for subgroup in subgroups:
        subgroup(c, p.children)


def _set_scientific_properties(c):
    """Set component scientific properties.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    """
    # TODO group existing properties under this umbrella
    pass


def _parse_components(c_tree):
    """Recursivley parses a component tree.

    :param c_tree: A set of model components.
    :type c_tree: list
    
    """
    for c in c_tree:
        _set_scientific_properties(c)
        _set_standard_properties(c)
        _parse_components(c.children)

                      
def parse(m):
    """Performs a parse over a model in readiness for later processing.

    :param m: A model component.
    :type m: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: A model component.
    :rtype: pyesdoc.ontologies.cim.v1.software.ModelComponent

    """
    # Parse set of child components.
    _parse_components(m.children)

    return m
