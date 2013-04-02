# Module imports.
from esdoc_api.models.entities import FacetRelation
from esdoc_api.models.entities import FacetRelationType
from esdoc_api.models.entities import FacetType
from esdoc_api.models.entities import Facet


# Module exports.
__all__ = [
    'get_facet',
    'set_facet_relation',
    'get_facet_values',
    'get_facet_relations'
]


def get_facet(ft, key, value, value_for_display=None, key_for_sort=None):
    """Returns a facet (creating it if necessary).

    :param ft: Facet type.
    :param key: Facet key.
    :param key_for_sort: Facet sort key.
    :param value: Facet value.
    :param value_for_display: Facet display value.
    :type ft: esdoc_api.models.entities.entity.FacetType
    :type key: str
    :type key_for_sort: str
    :type value: str
    :type value_for_display: str

    :returns: A facet instance.
    :rtype: esdoc_api.models.entities.entity.Facet

    """
    if isinstance(ft, FacetType) == False:
        raise TypeError('ft param is of invalid type')

    # Get from cached collection.
    f = ft.get_value(key[:2047])

    # Get from database.
    if f is None:
        f = Facet.retrieve(ft, key)
        if f is not None:
            ft.Values.append(f)

    # Create if necessary.
    if f is None:
        f = Facet()
        f.Type_ID = ft.ID
        f.Key = key[:2047]
        if key_for_sort is not None:
            f.KeyForSort = key_for_sort[:2047]
        f.Value = value[:2047]
        if value_for_display is not None:
            f.ValueForDisplay = value_for_display[:2047]
        ft.Values.append(f)
        
    return f


def set_facet_relation(frt, from_facet, to_facet):
    """Creates a facet relation (if necessary).

    :param frt: Facet relation type.
    :param from_facet: From facet.
    :param to_facet: To facet.
    :type type: esdoc_api.models.entities.entity.FacetRelationType
    :type from_facet: esdoc_api.models.entities.entity.Facet
    :type to_facet: esdoc_api.models.entities.entity.Facet

    """
    if isinstance(frt, FacetRelationType) == False:
        raise TypeError('frt param is of invalid type')
    if isinstance(from_facet, Facet) == False:
        raise TypeError('from_facet param is of invalid type')
    if isinstance(to_facet, Facet) == False:
        raise TypeError('to_facet param is of invalid type')

    fr = FacetRelation.retrieve(frt, from_facet, to_facet)
    if fr is None:
        fr = FacetRelation()
        fr.Type = frt
        fr.From = from_facet
        fr.To = to_facet


def get_facet_values(type):
    return FacetType.get_values(type)


def get_facet_relations(type):    
    return FacetRelationType.get_relations(type)
