"""
.. module:: esdoc_api.lib.repo.index.cim_v1.model_component.reducer.py
   :platform: Unix, Windows
   :synopsis: Reduces a cim.v1.software.model_component document in readiness for facet emission.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""

def _component_predicate(c):
    """Determines whether a component is in scope or not.

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: A flag indicating whether the component is in scope or not for further processing.
    :rtype: bool
    
    """
    return True


def _property_predicate(p):
    """Determines whether a component property is in scope or not.

    :param p: A model component property.
    :type p: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    :returns: A flag indicating whether the component property is in scope or not for further processing.
    :rtype: bool

    """
    return len(p.values) > 0 or len(p.children) > 0


def _reduce_values(memo, v_list):
    """Reduces a set of component property values.

    :param memo: A set of component property values.
    :type memo: list

    :param v_list: Set of component property values.
    :type v_list: list

    :returns: A set of component property values.
    :rtype: list

    """
    memo.extend(v_list)
    
    return memo


def _reduce_properties(memo, c, p_tree, parent=None):
    """Reduces a set of component properties.

    :param memo: A set of component properties.
    :type memo: list

    :param c: A model component.
    :type c: pyesdoc.ontologies.cim.v1.software.ModelComponent
    
    :param p_tree: Set of component properties.
    :type p_tree: list

    :param parent: The parent property.
    :type parent: pyesdoc.ontologies.cim.v1.software.ComponentProperty

    :returns: A set of component properties.
    :rtype: list

    """
    # Extend property attributes.
    for p in [i for i in p_tree]:
        p.component = c
        p.parent = parent

    # Reduce property tree.
    for p in [i for i in p_tree if _property_predicate(i)]:
        memo.append((p, _reduce_values([], p.values)))
        if len(p.children) > 0:
            _reduce_properties(memo, c, p.children, p)
            
    return memo


def _reduce_components(memo, c_tree, parent=None):
    """Reduces a set of components.

    :param memo: A set of components.
    :type memo: list

    :param c_tree: Set of components.
    :type c_tree: list

    :param parent: The parent component.
    :type parent: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: A set of components.
    :rtype: list

    """
    # Extend component attributes.
    for c in [i for i in c_tree]:
        c.parent = parent
        
    # Reduce component tree.
    for c in [i for i in c_tree if _component_predicate(i)]:
        memo.append((c, _reduce_properties([], c, c.properties)))
        if len(c.children) > 0:
            _reduce_components(memo, c.children, c)
            
    return memo


def reduce(m):
    """Performs a reduce (fold) over a model in readiness for later processing.

    :param m: A model component.
    :type m: pyesdoc.ontologies.cim.v1.software.ModelComponent

    :returns: A tuple containing the model and it's reduced components.
    :rtype: tuple

    """
    return (m, _reduce_components([], m.children))
