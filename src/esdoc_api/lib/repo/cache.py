"""
.. module:: prodiguer_shared.repo.cache.py
   :copyright: Copyright "Jun 12, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Static cache of repo entities.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.models as models
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.utils.runtime as rt



# Cache (simple dictionary for now).
_cache = {}

# Set of targets for caching.
_cache_targets = (
    ('DocumentEncoding', models.DocumentEncoding, 'Encoding'),
    ('DocumentLanguage', models.DocumentLanguage, 'Code'),
    ('DocumentOntology', models.DocumentOntology, 'FullName'),
    ('DocumentType', models.DocumentType, 'Key'),
    ('IngestState', models.IngestState, 'Name'),
    ('Institute', models.Institute, 'Name'),
    ('Project', models.Project, 'Name'),
)


def _assert_collection(collection):
    """Asserts that the the collection is an iterable.
    
    :param collection: Cache collection.
    :type collection: iterable
    
    """
    rt.assert_typed_iter(collection,
                         models.Entity,
                         "All collection items must be sub-classes of models.Entity.")


def _assert_collection_key(key):
    """Asserts that the the collection key is supported.

    :param key: Cache collection key.
    :type key: str

    :param must_exist: Flag indicating whether the assertion is a positive (True) or negative (False) one.
    :type must_exist: bool

    """
    def get_msg():
        return "Cache collection ({0}) has not been regsitered.".format(key)
    
    rt.assert_iter_item(_cache, _format_key(key), get_msg)


def _format_key(key):
    """Returns formatted cache key.

    :param key: Key to uniquely identify a cache collection / item.
    :type key: object

    :returns: Formatted cache item key.
    :rtype: str
    
    """
    return str(key).upper()


def register(collection_key, collection, item_key_attribute='Name'):
    """Registers a collection with the cache.

    :param collection_key: Cache collection key.
    :type collection_key: str
    
    :param collection: Cache collection.
    :type collection: iterable

    :param item_key_attribute: Attribute on collection items from which to derive key.
    :type item_key_attribute: str

    """
    # Denfensive programming.
    _assert_collection(collection)

    def get_collection():
        result = {}
        for i in collection:
            result[_format_key(getattr(i, item_key_attribute))] = i
            result[_format_key(i.ID)] = i
        return result
    
    _cache[_format_key(collection_key)] = get_collection()


def load():
    """Loads cache.

    """
    for key, type, attribute in _cache_targets:
        register(key, dao.get_all(type), attribute)


def unload():
    """Unloads cache.

    """
    for key in _cache.keys():
        del _cache[key]


def is_cached(collection_key, item_key=None):
    """Returns whether either a cache collection or a cache item exists or not.

    :param collection: Cache collection key.
    :type collection: str

    :param item_key: Cache item key.
    :type item_key: str

    :returns: True if target is cached, False otherwise.
    :rtype: bool

    """
    if item_key is None:
        return _format_key(collection_key) in _cache.keys()
    else:
        _assert_collection_key(collection_key)
        return _format_key(item_key) in _cache[_format_key(collection_key)]


def get(collection_key, item_key=None):
    """Returns either a cached object or an attribute upon a cached object.

    :param collection: Cache collection key.
    :type collection: str

    :param item_key: Cache item key.
    :type item_key: str or None

    :returns: Either a cached collection or a cached item, otherwise None.
    :rtype: None or sub-class of models.Entity or list

    """
    # Defensive programming.
    _assert_collection_key(collection_key)

    collection = _cache[_format_key(collection_key)]

    if item_key is None:
        return collection
    else:
        item_key = _format_key(item_key)
        if item_key in collection:
            return collection[item_key]
        else:
            return None


def get_names(collection_key, 
              name_attr='Name',
              name_formatter=lambda x : x.lower()):
    """Returns list of names.

    :param collection: Cache collection key.
    :type collection: str

    :param name_attr: Cache item name attribute.
    :type name_attr: str

    :param name_formatter: Cache item name formatter.
    :type name_formatter: str

    :returns: List of names.
    :rtype: list

    """
    # Defensive programming.
    _assert_collection_key(collection_key)

    return map(lambda x : name_formatter(getattr(x, name_attr)),
               _cache[_format_key(collection_key)].values())


def get_count(collection_key=None):
    """Returns the count of cached collections.

    :returns: The count of cached collections.
    :rtype: int

    """
    if collection_key is None:
        return len(_cache)
    else:
        _assert_collection_key(collection_key)
        return len(_cache[_format_key(collection_key)])


def get_id(collection_key, item_key):
    """Helper function to return a cached item's ID.

    :param collection_key: Cache collection key.
    :type collection_key: str

    :param item_key: Cache item key.
    :type item_key: str

    :returns: None or an entity ID if cached.
    :rtype: None or int

    """
    item = get(collection_key, item_key)
    
    return None if item is None else item.ID


def get_document_encoding(encoding_name=None):
    """Returns either all document encodings or first document encoding with matching name.

    :param encoding_name: Document encoding name.
    :type encoding_name: str

    """
    return get('DocumentEncoding', encoding_name)


def get_document_language(language_name=None):
    """Returns either all document languages or first document language with matching name.

    :param language_name: Document language name.
    :type language_name: str

    """
    return get('DocumentLanguage', language_name)


def get_document_ontology(ontology_name=None, ontology_version=None):
    """Returns either all document ontologies or first document ontology with matching name.

    :param ontology_name: Document ontology name.
    :type ontology_name: str

    :param ontology_version: Document ontology version.
    :type ontology_version: str

    """
    if ontology_name is None:
        return get('DocumentOntology')

    for ontology in get('DocumentOntology').values():
        if ontology.Name.upper() == ontology_name.upper() and \
           ontology.Version.upper() == ontology_version.upper() :
           return ontology

    return None



def get_document_type(type_name=None):
    """Returns either all document types or first document type with matching name.

    :param type_name: Document type name.
    :type type_name: str

    """
    return get('DocumentType', type_name)


def get_ingest_state(ingest_state_name=None):
    """Returns either all ingest states or first ingest state with matching name.

    :param ingest_state_name: Ingest state name.
    :type ingest_state_name: str

    """
    return get('IngestState', ingest_state_name)


def get_institute(institute_name=None):
    """Returns either all institutes or first institute with matching name.

    :param institute_name: Institute name.
    :type institute_name: str

    """
    return get('Institute', institute_name)


def get_project(project_name=None):
    """Returns either all projects or first project with matching name.

    :param project_name: Project name.
    :type project_name: str

    """
    return get('Project', project_name)


