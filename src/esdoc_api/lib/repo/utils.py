"""
.. module:: esdoc_api.lib.repo.utils.py
   :copyright: Copyright "Jul 2, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Repository utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from esdoc_api.models.vocab import DocumentEncoding
from esdoc_api.models.vocab import DocumentOntology
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.utils.runtime as rt
from esdoc_api.models import (
    supported_types,
    Document,
    DocumentDRS,
    DocumentExternalID,
    DocumentLanguage,
    DocumentRepresentation,
    DocumentSubDocument,
    DocumentSummary,
    Facet,
    FacetRelation,
    FacetRelationType,
    FacetType,
    IngestEndpoint,
    Project,
    DOCUMENT_VERSION_ALL,
    )


# Default drs split.
_DRS_SPLIT = '/'


def create(type):
    """Creates a type instance and appends to current session.

    :param type: A domain model type.
    :type type: class

    :returns: An instance of passed domain model type.
    :rtype: A sub-class of esdoc_api.models.Entity

    """
    rt.assert_iter_item(supported_types, type, "Unknown model type.")
    
    instance = type()
    session.insert(instance, auto_commit=False)

    return instance


def create_document(project, endpoint, as_obj):
    """Creates & returns a Document instance.

    :param project: Project with which document is associated.
    :type project: esdoc_api.models.Project

    :param endpoint: Endpoint from which document was ingested.
    :type endpoint: esdoc_api.models.IngestEndpoint

    :param as_obj: pyesdoc document object representation.
    :type as_obj: object

    """
    # Defensive programming.
    rt.assert_var('project', project, Project)
    rt.assert_var('endpoint', endpoint, IngestEndpoint)
    rt.assert_pyesdoc_var('as_obj', as_obj)

    # Instantiate & assign attributes.
    instance = dao.get_document(project.ID,
                                str(as_obj.cim_info.id),
                                str(as_obj.cim_info.version))
    if instance is None:
        instance = create(Document)
        instance.as_obj = as_obj
        instance.Project_ID = project.ID
        instance.IngestEndpoint_ID = endpoint.ID
        instance.UID = str(as_obj.cim_info.id)
        instance.Version = int(as_obj.cim_info.version)
        instance.Type = as_obj.cim_info.type_info.type.upper()
        set_document_name(instance, as_obj)
        set_document_is_latest_flag(instance, project)

    return instance


def create_sub_document(parent, child):
    """Creates & returns a DocumentSubDocument instance.

    :param parent: Parent document.
    :type parent: esdoc_api.models.Document

    :param child: Child document.
    :type child: esdoc_api.models.Document

    :returns: SubDocument instance.
    :rtype: esdoc_api.models.DocumentSubDocument

    """
    # Defensive programming.
    rt.assert_var('parent', parent, Document)
    rt.assert_var('child', child, Document)

    # Ensure parent's sub-document collection is upto date.
    if child not in parent.children:
        parent.children.append(child)

    # Instantiate & assign attributes.
    instance = dao.get_document_sub_document(parent.ID, child.ID)
    if instance is None:
        instance = create(DocumentSubDocument)
        instance.Document_ID = parent.ID
        instance.SubDocument_ID = child.ID
        parent.HasChildren = True

    return instance


def set_document_is_latest_flag(document, project):
    """Sets flag indicating whether a document is the latest version or not.

    :param document: Document whose is_latest flag is being assigned.
    :type document: esdoc_api.models.Document

    :param project: Project with which document is associated.
    :type project: esdoc_api.models.Project

    """    
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_var('project', project, Project)

    # Get all related documents and update IsLatest flag accordingly.
    all = dao.get_document(project.ID, document.UID, DOCUMENT_VERSION_ALL)
    for i in range(len(all)):
        all[i].IsLatest = (i == 0)
        if all[i].Version == document.Version:
            document.IsLatest == all[i].IsLatest


def get_document_name(as_obj):
    """Gets document name.

    :param as_obj: pyesdoc document object representation.
    :type as_obj: object

    """
    # Defensive programming.
    rt.assert_pyesdoc_var('as_obj', as_obj)

    # Default name setter.
    def _default():
        return as_obj.short_name

    # Custom name setters.
    def _for_cim_1_data_object():
        return as_obj.acronym

    def _for_cim_1_grid_spec():
        if len(as_obj.esm_model_grids) > 0:
            return as_obj.esm_model_grids[0].short_name
        return None

    def _for_cim_1_quality():
        if len(as_obj.reports) > 0 and \
           as_obj.reports[0].measure is not None:
            return as_obj.reports[0].measure.name
        return None

    # Getter functions organised by document type.
    getters = {
        'cim' : {
            '1' : {
                'dataObject' : _for_cim_1_data_object,
                'ensemble' : _default,
                'gridSpec' : _for_cim_1_grid_spec,
                'statisticalModelComponent' : _default,
                'modelComponent' : _default,
                'numericalExperiment' : _default,
                'simulationRun' : _default,
                'platform' : _default,
                'cIM_Quality' : _for_cim_1_quality,
            }
        }
    }

    # Assign getter.
    getter = None
    ontology_name = as_obj.cim_info.type_info.ontology_name
    if ontology_name in getters:
        ontology_version = as_obj.cim_info.type_info.ontology_version
        if ontology_version in getters[ontology_name]:
            type_name = as_obj.cim_info.type_info.type
            if type_name in getters[ontology_name][ontology_version]:
                getter = getters[ontology_name][ontology_version][type_name]
    
    return None if getter is None else getter()


def set_document_name(document, as_obj):
    """Sets document name.

    :param document: Document whose name is being assigned.
    :type document: esdoc_api.models.Document

    :param as_obj: pyesdoc document object representation.
    :type as_obj: object

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    
    document.Name = get_document_name(as_obj)


def create_document_drs(document, keys):
    """Factory method to create and return a DocumentDRS instance.

    :param document: A deserialized Document instance.
    :type document: esdoc_api.models.Document

    :param keys: Set of DRS keys.
    :type keys: list

    :returns: A DocumentDRS instance.
    :rtype: esdoc_api.models.DocumentDRS

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_typed_iter(keys, str)

    # Reformat path.
    path = _DRS_SPLIT.join(keys).upper()

    # Create (only if necessary).
    instance = dao.get_document_drs(document.Project_ID, document.ID, path)
    if instance is None:
        instance = create(DocumentDRS)
        instance.Document_ID = document.ID
        instance.Path = path
        instance.Project_ID = document.Project_ID
        for i in range(len(keys)):
            if i > 7:
                break;
            elif keys[i] is not None:
                setattr(instance, "Key_0" + str(i + 1), keys[i].upper())

    return instance


def create_document_external_ids(document, first_only=False):
    """Factory method to create and return a list of DocumentExternalID instances.

    :param document: A deserialized Document instance.
    :type document: esdoc_api.models.Document

    :param first_only: Flag indicating whether only the first external id will be returned.
    :type first_only: bool

    :returns: A DocumentExternalID instance.
    :rtype: esdoc_api.models.DocumentExternalID

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_var('first_only', first_only, bool)
    rt.assert_pyesdoc_var('document.as_obj', document.as_obj)
    
    for id in document.as_obj.cim_info.external_ids:
        instance = dao.get_document_external_id(document.Project_ID,
                                                document.ID,
                                                id.value.upper())
        if instance is None:
            instance = create(DocumentExternalID)
            instance.Project_ID = document.Project_ID
            instance.Document_ID = document.ID
            instance.ExternalID = id.value.upper()
        if first_only:
            break

    return dao.get_document_external_ids(document.ID, document.Project_ID)


def create_document_summary(document, language):
    """Factory method to create and return a DocumentSummary instance.

    :param document: A deserialized Document instance.
    :type document: esdoc_api.models.Document

    :param language: A DocumentLanguage instance.
    :type language: esdoc_api.models.DocumentLanguage

    :returns: A DocumentSummary instance.
    :rtype: esdoc_api.models.DocumentSummary

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_var('language', language, DocumentLanguage)
    
    instance = dao.get_document_summary(document.ID, language.ID)
    if instance is None:
        instance = create(DocumentSummary)
        instance.Document_ID = document.ID
        instance.Language_ID = language.ID
    set_document_summary_fields(document, instance)

    document.Summaries = [s for s in document.Summaries if s.ID != instance.ID]
    document.Summaries.append(instance)
    
    return instance


def get_document_summary_fields(document):
    """Returns document summary fields.

    :param summary: Document whose summary fields are being derived.
    :type summary: esdoc_api.models.Document

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_pyesdoc_var('document.as_obj', document.as_obj)

    as_obj = document.as_obj

    def _for_default():
        return (
            as_obj.short_name,
            as_obj.long_name
        )

    def _for_cim_1_cim_quality():
        return (
            as_obj.cim_info.id,
            as_obj.cim_info.version,
            None if not len(as_obj.cim_info.external_ids) else as_obj.cim_info.external_ids[0].value
        )

    def _for_cim_1_data_object():
        return (
            as_obj.acronym,
            as_obj.description
        )

    def _for_cim_1_grid_spec():
        if len(as_obj.esm_model_grids) > 0:
            return (
                as_obj.esm_model_grids[0].short_name,
                as_obj.esm_model_grids[0].long_name
            )

    def _for_cim_1_model_component():
        return (
            as_obj.short_name,
            as_obj.long_name,
            None if as_obj.release_date is None else str(as_obj.release_date)
        )
        
    # Getter functions organised by document type.
    getters = {
        'cim' : {
            '1' : {
                'cIM_Quality' : _for_cim_1_cim_quality,
                'dataObject' : _for_cim_1_data_object,
                'ensemble' : _for_default,
                'gridSpec' : _for_cim_1_grid_spec,
                'modelComponent' : _for_cim_1_model_component,
                'statisticalModelComponent' : _for_cim_1_model_component,
                'numericalExperiment' : _for_default,
                'simulationRun' : _for_default,
                'platform' : _for_default,
            }
        }
    }

    # Assign getter.
    getter = None
    ontology_name = as_obj.cim_info.type_info.ontology_name
    if ontology_name in getters:
        ontology_version = as_obj.cim_info.type_info.ontology_version
        if ontology_version in getters[ontology_name]:
            type_name = as_obj.cim_info.type_info.type
            if type_name in getters[ontology_name][ontology_version]:
                getter = getters[ontology_name][ontology_version][type_name]
    
    return None if getter is None else getter()


def set_document_summary_fields(document, summary):
    """Sets document summary fields.

    :param summary: Document whose summary fields are being assigned.
    :type summary: esdoc_api.models.Document

    :param summary: Summary whose fields are being assigned.
    :type summary: esdoc_api.models.DocumentSummary

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_var('summary', summary, DocumentSummary)

    fields = get_document_summary_fields(document)
    for i in range(len(fields)):
        setattr(summary, 'Field_0' + str(i + 1), str(fields[i]))


def create_facet_relation(frt, from_facet, to_facet):
    """Creates a facet relation (if necessary).

    :param frt: Facet relation type.
    :type frt: esdoc_api.models.FacetRelationType

    :param from_facet: From facet.
    :type from_facet: esdoc_api.models.Facet

    :param to_facet: To facet.
    :type to_facet: esdoc_api.models.Facet

    """
    # Defensive programming.
    rt.assert_var('frt', frt, FacetRelationType)
    rt.assert_var('from_facet', from_facet, Facet)
    rt.assert_var('to_facet', to_facet, Facet)

    fr = dao.get_facet_relation(frt.ID, from_facet.ID, to_facet.ID)
    if fr is None:
        fr = create(FacetRelation)
        fr.Type_ID = frt.ID
        fr.From_ID = from_facet.ID
        fr.To_ID = to_facet.ID
        
    return fr


def create_facet(ft, key, value, value_for_display=None, key_for_sort=None):
    """Creates a facet (if necessary).

    :param ft: Facet type.
    :type ft: esdoc_api.models.FacetType

    :param key: Facet key.
    :type key: str

    :param key_for_sort: Facet sort key.
    :type key_for_sort: str

    :param value: Facet value.
    :type value: str

    :param value_for_display: Facet display value.
    :type value_for_display: str

    :returns: A facet instance.
    :rtype: esdoc_api.models.Facet

    """
    # Defensive programming.
    rt.assert_var('ft', ft, FacetType)
    rt.assert_var('key', key, str)
    rt.assert_var('value', value, str)
    rt.assert_optional_var('value_for_display', value_for_display, str)
    rt.assert_optional_var('key_for_sort', key_for_sort, str)

    # Get from cached collection.
    f = ft.get_value(key[:2047])

    # Get from database.
    if f is None:
        f = dao.get_facet(ft.ID, key)
        if f is not None and \
           len([i for i in ft.Values if i.ID == f.ID]) == 0:
            ft.Values.append(f)

    # Create if necessary.
    if f is None:
        f = create(Facet)
        f.Type_ID = ft.ID
        f.Key = key[:2047]
        f.Value = value[:2047]
        if value_for_display is not None:
            f.ValueForDisplay = value_for_display[:2047]
        if key_for_sort is not None:
            f.KeyForSort = key_for_sort[:2047]
        ft.Values.append(f)

    return f


def create_document_representation(document, 
                                   ontology,
                                   encoding,
                                   language,
                                   representation):
    """Factory method to create a document representation.

    :param document: The document to which a representation is being assigned.
    :type document: esdoc_api.models.document.Document

    :param ontology: Document ontology.
    :type ontology: esdoc_api.models.DocumentOntology

    :param encoding: Document representation encoding.
    :type encoding: esdoc_api.models.document_encoding.DocumentEncoding

    :param language: Document representation language.
    :type language: esdoc_api.models.document_language.DocumentLanguage

    :param representation: Document representation, e.g. json | xml.
    :type representation: unicode

    :returns: A document representation.
    :rtype: esdoc_api.models.document_representation.DocumentRepresentation

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_var('ontology', ontology, DocumentOntology)
    rt.assert_var('encoding', encoding, DocumentEncoding)
    rt.assert_var('language', language, DocumentLanguage)
    rt.assert_var('representation', representation, unicode)

    # Update or create as appropriate.
    instance = dao.get_document_representation(document.ID,
                                               ontology.ID,
                                               encoding.ID,
                                               language.ID)
    if instance is None:
        instance = create(DocumentRepresentation)
        instance.Document_ID = document.ID
        instance.Ontology_ID = ontology.ID
        instance.Encoding_ID = encoding.ID
        instance.Language_ID = language.ID
    instance.Representation = representation

    return instance


def get_document_representation(document, ontology, encoding, language):
    """Loads a document representation.

    :param document: A document for which a representation is being retrieved.
    :type document: esdoc_api.models.document.Document

    :param ontology: Document ontology.
    :type ontology: esdoc_api.models.DocumentOntology

    :param encoding: Associated document encoding.
    :type encoding: esdoc_api.models.document.Document

    :param language: Associated document language.
    :type language: esdoc_api.models.document.Document

    :returns: A document representation.
    :rtype: esdoc_api.models.document_representation.DocumentRepresentation

    """
    # Defensive programming.
    rt.assert_var('document', document, Document)
    rt.assert_var('ontology', ontology, DocumentOntology)
    rt.assert_var('encoding', encoding, DocumentEncoding)
    rt.assert_var('language', language, DocumentLanguage)

    instance = dao.get_document_representation(document.ID,
                                               ontology.ID,
                                               encoding.ID,
                                               language.ID)

    return None if instance is None else instance.Representation


def get_facets(type_name):
    """Maps a a list of Facet instances by their FacetType name to list of lists.

    :param type_name: Name of a FacetType.
    :type type_name: str

    :returns: List of Facet instances with matching FacetType name.
    :rtype: list

    """
    result = []

    ft = dao.get_by_name(FacetType, type_name)
    if ft is not None:
        for v in ft.Values:
            item = [v.ID, v.Key, v.Value, '', '']
            if v.KeyForSort:
                item[3] = v.KeyForSort
            if v.ValueForDisplay:
                item[4] = v.ValueForDisplay
            result.append(item)

    return sorted(result, key=lambda v: v[2])


def get_facet_relations(type_name):
    """Maps a a list of FacetRelation instances by their FacetRelationType name to list of lists.

    :param type_name: Name of a FacetRelationType.
    :type type_name: str

    :returns: List of FacetRelation instances with matching FacetRelationType name.
    :rtype: list

    """
    result = []

    frt = dao.get_by_name(FacetRelationType, type_name)
    if frt is not None:
        for r in frt.Relations:
            result.append([r.From_ID, r.To_ID])

    return sorted(result, key=lambda r: r[0])


def get_document_by_obj(project_id, as_obj):
    """Returns a Document instance by it's project and pyesdoc object representation.

    :param project_id: ID of a Project instance.
    :type project_id: int

    :param as_obj: pyesdoc document object representation.
    :type as_obj: object

    :returns: First matching document.
    :rtype: esdoc_api.models.Document

    """
    # Retrieve.
    doc_info = as_obj.cim_info
    instance = dao.get_document(project_id, doc_info.id, doc_info.version)

    # Assign.
    if instance is not None:
        instance.as_obj = as_obj

    return instance

