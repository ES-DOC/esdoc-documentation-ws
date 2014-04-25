"""
.. module:: esdoc_api_test.test_repo_cache.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Repository cache functional tests.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""

# Module imports.
import nose.tools 

import esdoc_api.lib.repo.cache as cache
import esdoc_api.models as models
import esdoc_api.lib.utils.runtime as rt
import esdoc_api_test.utils as tu

# Known collections info.
_COLLECTIONS = (
    ('IngestState', 5, 'queued', models.IngestState),
    ('Institute', 29, 'ipsl', models.Institute),
    ('DocumentEncoding', 3, 'json', models.DocumentEncoding),
    ('DocumentLanguage', 139, 'aa', models.DocumentLanguage),
    ('DocumentOntology', 1, 'cim-v1', models.DocumentOntology),
    ('DocumentType', 10, 'cim_quality', models.DocumentType),
    ('Project', 3, 'cmip5', models.Project),
)


def _setup():
    cache.load()


def _teardown():
    cache.unload()


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_count_01():
    tu.assert_int(cache.get_count(), len(_COLLECTIONS), tu.COMPARE_GTE)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_count_02():
    for info in _COLLECTIONS:
        tu.assert_int(cache.get_count(info[0]), info[1], tu.COMPARE_GTE)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_load():
    tu.assert_int(cache.get_count(), len(_COLLECTIONS))
    for info in _COLLECTIONS:
        tu.assert_int(cache.get_count(info[0]), info[1], tu.COMPARE_GTE)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_unload():
    cache.unload()
    tu.assert_int(cache.get_count(), 0)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_register_01():
    class TestModelA(models.Entity):
        __tablename__ = 'tblTest'
        __table_args__ = (
            {'schema' : 'Test'}
        )

        def __init__(self):
            self.Name = "Test"

    count = cache.get_count()
    cache.register('Test', [TestModelA()])
    tu.assert_int(cache.get_count(), count + 1)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
@nose.tools.raises(rt.ESDOC_API_Error)
def test_register_02():
    class TestModelA(object):
        def __init__(self):
            self.Name = "Test"
            
    cache.register('Test', [TestModelA()])


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_is_cached_01():
    for info in _COLLECTIONS:
        assert cache.is_cached(info[0])
    assert not cache.is_cached('XXX')


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_is_cached_02():
    for info in _COLLECTIONS:
        assert cache.is_cached(info[0], info[2])
        for i in range(info[1]):
            assert cache.is_cached(info[0], i + 1)
        assert not cache.is_cached(info[0], 'XXX')


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_01():
    for info in _COLLECTIONS:
        collection = cache.get(info[0])
        tu.assert_object(collection, dict)
        tu.assert_iter(collection,
                             length=info[1],
                             length_compare=tu.COMPARE_GTE,
                             item_type=info[3])


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_02():
    for info in _COLLECTIONS:
        collection = cache.get(info[0])
        for key, instance1 in collection.items():
            instance2 = cache.get(info[0], key)
            tu.assert_object(instance2, info[3])
            tu.assert_objects(instance1, instance2)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_id():
    for info in _COLLECTIONS:
        collection = cache.get(info[0])
        for instance1 in collection.values():
            instance2 = cache.get(info[0], instance1.ID)
            tu.assert_object(instance2, info[3])
            tu.assert_objects(instance1, instance2)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_doc_encoding():
    tu.assert_iter(cache.get_doc_encoding(), length=5, item_type=models.DocumentEncoding)
    tu.assert_object(cache.get_doc_encoding('json'), models.DocumentEncoding)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_doc_language():
    tu.assert_iter(cache.get_doc_language(), length=139, item_type=models.DocumentLanguage)
    tu.assert_object(cache.get_doc_language('aa'), models.DocumentLanguage)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_doc_ontology():
    tu.assert_iter(cache.get_doc_ontology(), length=1, item_type=models.DocumentOntology)
    tu.assert_object(cache.get_doc_ontology('cim.1'), models.DocumentOntology)
    tu.assert_object(cache.get_doc_ontology('cim', '1'), models.DocumentOntology)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_doc_type():
    tu.assert_iter(cache.get_doc_type(), length=1, item_type=models.DocumentType)
    tu.assert_object(cache.get_doc_type('modelComponent'), models.DocumentType)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_ingest_state():
    tu.assert_iter(cache.get_ingest_state(), length=5, item_type=models.IngestState)
    tu.assert_object(cache.get_ingest_state('queued'), models.IngestState)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_institute():
    tu.assert_iter(cache.get_institute(), length=29, item_type=models.Institute)
    tu.assert_object(cache.get_institute('ipsl'), models.Institute)


@nose.tools.with_setup(setup=_setup, teardown=_teardown)
def test_get_project():
    tu.assert_iter(cache.get_project(), length=3, item_type=models.Project)
    tu.assert_object(cache.get_project('cmip5'), models.Project)
