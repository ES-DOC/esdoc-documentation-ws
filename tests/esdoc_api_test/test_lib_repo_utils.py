"""
.. module:: esdoc_api_test.test_repo_utils.py

   :copyright: @2013 Institute Pierre Simon Laplace (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Repository utility functional tests.

.. moduleauthor:: Institute Pierre Simon Laplace (ES-DOC) <dev@es-doc.org>

"""
# Module imports.
import uuid

from nose.tools import with_setup

import esdoc_api_test.utils as tu
import esdoc_api.lib.repo.dao as dao
import esdoc_api.models as models
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.repo.utils as utils
from esdoc_api.lib.pyesdoc.ontologies.cim.v1.types import StandardName



def _teardown():
    session.rollback()


@with_setup(teardown=_teardown)
def test_create():
    document = utils.create(models.Document)
    tu.assert_object(document, models.Document)


@with_setup(teardown=_teardown)
def test_create_doc():
    document1 = tu.get_test_document() # N.B. implicity calls utils.create_doc
    tu.assert_object(document1, models.Document)

    id = str(uuid.uuid1())
    version = tu.get_int()
    document = tu.get_test_document(id, version)
    tu.assert_str(id, document.UID)
    tu.assert_int(version, document.Version)

    project = tu.get_test_model(models.Project)
    document1 = tu.get_test_document(project=project)
    document2 = tu.get_test_document(document1.UID, document1.Version, project=project)
    tu.assert_entity(document1, document2)
    

@with_setup(teardown=_teardown)
def test_set_doc_is_latest_flag():
    project = tu.get_test_model(models.Project)
    document1 = tu.get_test_document(project=project)
    assert document1.IsLatest == True
    
    document2 = tu.get_test_document(document1.UID, document1.Version + 1, project=project)
    tu.assert_int(document2.Version, document1.Version + 1)
    assert document2.IsLatest == True
    assert document1.IsLatest == False
    

@with_setup(teardown=_teardown)
def test_get_doc_name():
    doc = tu.get_test_pyesdoc_doc()
    tu.assert_str(utils.get_doc_name(doc), "HadGEM2-A")
    doc.short_name = "XXX"
    tu.assert_str(utils.get_doc_name(doc), "XXX")


@with_setup(teardown=_teardown)
def test_create_doc_drs():
    document = tu.get_test_document()
    path = reduce(lambda path, i: path + "/Key_" + str(i + 1), range(8), "")[1:]
    keys = path.split('/')
    drs = utils.create_doc_drs(document, path.split('/'))

    tu.assert_object(drs, models.DocumentDRS)
    assert drs.Path == path.upper()
    for i in range(8):
        assert getattr(drs, 'Key_0' + str(i + 1)) == keys[i]


@with_setup(teardown=_teardown)
def test_create_doc_external_ids():
    document = tu.get_test_document()
    tu.assert_int(0, len(dao.get_document_external_ids(document.ID, document.Project_ID)))

    external_id = StandardName()
    external_id.value = tu.get_uuid()
    document.as_obj.meta.external_ids.append(external_id)

    utils.create_doc_external_ids(document)
    tu.assert_int(1, len(dao.get_document_external_ids(document.ID, document.Project_ID)))


@with_setup(teardown=_teardown)
def test_create_doc_summary():
    document = tu.get_test_document()
    language1 = tu.get_test_model(models.DocumentLanguage)
    language2 = tu.get_test_model(models.DocumentLanguage)

    summary1 = utils.create_doc_summary(document, language1)
    tu.assert_object(summary1, models.DocumentSummary)

    summary2 = utils.create_doc_summary(document, language2)
    tu.assert_object(summary2, models.DocumentSummary)

    tu.assert_str(document.as_obj.short_name, summary1.ShortName)
    tu.assert_str(document.as_obj.long_name, summary1.LongName)

    tu.assert_str(document.as_obj.short_name, summary2.ShortName)
    tu.assert_str(document.as_obj.long_name, summary2.LongName)

    summary1_ = utils.create_doc_summary(document, language1)
    tu.assert_entity(summary1, summary1_)

    summary2_ = utils.create_doc_summary(document, language2)
    tu.assert_entity(summary2, summary2_)


@with_setup(teardown=_teardown)
def test_get_doc_summary_fields():
    doc = tu.get_test_pyesdoc_doc()
    summary_fields = utils.get_doc_summary_fields(doc)

    tu.assert_iter(summary_fields, 3)
    tu.assert_str(summary_fields[0], "HadGEM2-A")
    tu.assert_str(summary_fields[1], "Hadley Global Environment Model 2 - Atmosphere")
    tu.assert_str(summary_fields[2], "2009-", True)

    
@with_setup(teardown=_teardown)
def test_set_doc_summary():
    document = tu.get_test_document()
    doc = document.as_obj
    language = tu.get_test_model(models.DocumentLanguage)
    summary = utils.create_doc_summary(document, language)

    tu.assert_str(doc.short_name, summary.ShortName)
    tu.assert_str(doc.long_name, summary.LongName)

    doc.short_name = "XXX"
    doc.long_name = "YYY"
    summary = utils.create_doc_summary(document, language)

    tu.assert_str(doc.short_name, summary.ShortName)
    tu.assert_str(doc.long_name, summary.LongName)


@with_setup(teardown=_teardown)
def test_create_facet_relation():
    # Create test objects.
    relation_type = tu.get_test_model(models.FacetRelationType)
    from_facet = tu.get_test_model(models.Facet)
    to_facet = tu.get_test_model(models.Facet)

    relation1 = utils.create_facet_relation(relation_type, from_facet, to_facet)
    tu.assert_object(relation1, models.FacetRelation)

    relation2 = utils.create_facet_relation(relation_type, from_facet, to_facet)
    tu.assert_entity(relation1, relation2)


@with_setup(teardown=_teardown)
def test_create_facet():
    # Create test objects.
    type = tu.get_test_model(models.FacetType)
    key = tu.get_string(127)
    value = tu.get_string(127)
    value_for_display = tu.get_string(127)
    key_for_sort = tu.get_string(127)

    # Create facet.
    facet1 = utils.create_facet(type, key, value, value_for_display, key_for_sort)
    tu.assert_object(facet1, models.Facet)
    tu.assert_object(facet1.Type, models.FacetType)
    tu.assert_entity(type, facet1.Type)
    tu.assert_in_collection(type.Values, None, facet1)
    values_length1 = len(type.Values)

    facet2 = utils.create_facet(type, key, value, value_for_display, key_for_sort)
    tu.assert_entity(facet1, facet2)
    tu.assert_in_collection(type.Values, None, facet1)
    tu.assert_int(values_length1, len(type.Values))

    type.Values = []
    facet3 = utils.create_facet(type, key, value, value_for_display, key_for_sort)
    tu.assert_entity(facet1, facet3)
    tu.assert_in_collection(type.Values, None, facet3)
    tu.assert_int(values_length1, len(type.Values))


@with_setup(teardown=_teardown)
def test_create_doc_representation():
    # Create test objects.
    document = tu.get_test_document()
    ontology = tu.get_test_model(models.DocumentOntology)
    encoding = tu.get_test_model(models.DocumentEncoding)
    language = tu.get_test_model(models.DocumentLanguage)
    as_unicode1 = tu.get_unicode(63)

    # Create representation.
    representation1 = utils.create_doc_representation(document,
                                                           ontology,
                                                           encoding,
                                                           language,
                                                           as_unicode1)
    tu.assert_object(representation1, models.DocumentRepresentation)
    tu.assert_unicode(representation1.Representation, as_unicode1)

    # Update representation.
    as_unicode2 = tu.get_unicode(63)
    representation2 = utils.create_doc_representation(document,
                                                           ontology,
                                                           encoding,
                                                           language,
                                                           as_unicode2)
    tu.assert_unicode(representation2.Representation, as_unicode2)
    tu.assert_int(representation1.ID, representation2.ID)

    language = tu.get_test_model(models.DocumentLanguage)
    representation3 = utils.create_doc_representation(document,
                                                           ontology,
                                                           encoding,
                                                           language,
                                                           as_unicode1)
    tu.assert_int_negative(representation1.ID, representation3.ID)    
    

@with_setup(teardown=_teardown)
def test_get_doc_representation():
    # Create test objects.
    document = tu.get_test_document()
    ontology = tu.get_test_model(models.DocumentOntology)
    encoding = tu.get_test_model(models.DocumentEncoding)
    language = tu.get_test_model(models.DocumentLanguage)
    as_unicode = tu.get_unicode(63)
    utils.create_doc_representation(document,
                                         ontology,
                                         encoding,
                                         language,
                                         as_unicode)

    # Create representation.
    representation = utils.get_doc_representation(document,
                                                       ontology,
                                                       encoding,
                                                       language)
    tu.assert_object(representation, unicode)
    tu.assert_unicode(representation, as_unicode)


@with_setup(teardown=_teardown)
def test_get_facets():
    # Create test objects.
    type = tu.get_test_model(models.FacetType)
    facet = utils.create_facet(type, tu.get_string(127), tu.get_string(127))
    tu.assert_iter(type.Values, 1)
    tu.assert_in_collection(type.Values, None, facet)

    facets = utils.get_facets(type.Name)    
    tu.assert_iter(facets, 1)
    tu.assert_int(facets[0][0], facet.ID)
    tu.assert_str(facets[0][1], facet.Key)
    tu.assert_str(facets[0][2], facet.Value)


@with_setup(teardown=_teardown)
def test_get_facet_relations():
    # Create test objects.
    type = tu.get_test_model(models.FacetRelationType)
    from_facet = utils.create_facet(tu.get_test_model(models.FacetType),
                                    tu.get_string(127),
                                    tu.get_string(127))
    to_facet = utils.create_facet(tu.get_test_model(models.FacetType),
                                  tu.get_string(127),
                                  tu.get_string(127))

    relation1 = utils.create_facet_relation(type, from_facet, to_facet)
    tu.assert_object(relation1, models.FacetRelation)

    relation2 = utils.create_facet_relation(type, from_facet, to_facet)
    tu.assert_entity(relation1, relation2)
    
    tu.assert_iter(type.Relations, 1)
    tu.assert_in_collection(type.Relations, None, relation1)

    relations = utils.get_facet_relations(type.Name)
    tu.assert_iter(relations, 1)
    tu.assert_int(relations[0][0], from_facet.ID)
    tu.assert_int(relations[0][1], to_facet.ID)


def test_get_doc_by_obj():
    # Tests retrieiving a Document instance by it's project and pyesdoc object representation.
    instance1 = tu.get_test_document()
    tu.assert_object(instance1.as_obj)
    instance2 = utils.get_doc_by_obj(instance1.Project_ID, instance1.as_obj)
    tu.assert_entity(instance1, instance2)