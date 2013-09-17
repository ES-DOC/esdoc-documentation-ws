"""
.. module:: esdoc_api.lib.repo.utils.py
   :copyright: Copyright "Jul 2, 2013", Earth System models.Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Repository utility functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import esdoc_api.lib.pyesdoc as pyesdoc
import esdoc_api.lib.repo.cache as cache
import esdoc_api.lib.repo.dao as dao
import esdoc_api.lib.repo.session as session
import esdoc_api.lib.utils.runtime as rt
import esdoc_api.models as models
import esdoc_api.lib.utils.cim_v1 as cim_v1



# Default drs split.
_DRS_SPLIT = '/'


def create(type):
    """Creates a type instance and appends to current session.

    :param type: A domain model type.
    :type type: class

    :returns: An instance of passed domain model type.
    :rtype: A sub-class of esdoc_api.models.Entity

    """
    rt.assert_iter_item(models.supported_types, type, "Unknown model type.")
    
    instance = type()
    session.insert(instance, auto_commit=False)

    return instance


def create_doc_from_json(doc_json):
    """Creates a document instance from a json blob.

    :param doc_json: A json blob.
    :type doc_json: unicode

    :returns: A document.
    :rtype: esdoc_api.models.Document

    """
    # Decode document from json.
    doc = pyesdoc.decode(doc_json, pyesdoc.ESDOC_ENCODING_JSON)
    if doc is None:
        rt.raise_error("Document could not be deserialized")

    # Derive project.
    project = cache.get_project(doc.doc_info.project)
    if project is None:
        rt.raise_error("Project {0} is unsupported".format(doc.doc_info.project))

    # Verify document does not already exist.
    if dao.get_document(project.ID, doc.doc_info.id, doc.doc_info.version) is not None:
        rt.raise_error("Document already exists")        

    # Derive institute.
    institute = cache.get_institute(doc.doc_info.institute)

    # Derive language.
    language = cache.get_doc_language(doc.doc_info.language)
    if language is None:
        rt.raise_error("Language {0} is unsupported".format(doc.doc_info.language))

    # Derive encoding.
    encoding = cache.get_doc_encoding(pyesdoc.ESDOC_ENCODING_JSON)

    # Derive ontology.
    ontology = get_doc_ontology(doc)
    if ontology is None:
        rt.raise_error("Ontology {0} is unsupported".format(doc.__class__.type_key))

    # Create document repository.
    document = create_doc(doc, project, None, institute)

    # Create document representation.
    create_doc_representation(document, ontology, encoding, language, doc_json)

    # Create document summary.
    create_doc_summary(document, language)

    # Create document external ID (i.e. simulation id).
    create_doc_external_ids(document)

    # Persist.
    session.commit()

    # Log.
    rt.log("CREATED DOC :: T={0} ID={1} UID={2} V={3}.".format(
        document.Type, document.ID, document.UID, document.Version))

    return {
        id : document.ID
    }


def update_doc_from_json(doc_json):
    """Updates a document instance from a json blob.

    :param doc_json: A json blob.
    :type doc_json: unicode

    :returns: A document.
    :rtype: esdoc_api.models.Document

    """
    # Decode document from json.
    doc = pyesdoc.decode(doc_json, pyesdoc.ESDOC_ENCODING_JSON)
    if doc is None:
        rt.raise_error("Document could not be deserialized")

    # Derive project.
    project = cache.get_project(doc.doc_info.project)
    if project is None:
        rt.raise_error("Project {0} is unsupported".format(doc.doc_info.project))

    # Derive institute.
    institute = cache.get_institute(doc.doc_info.institute)

    # Derive language.
    language = cache.get_doc_language(doc.doc_info.language)
    if language is None:
        rt.raise_error("Language {0} is unsupported".format(doc.doc_info.language))

    # Derive encoding.
    encoding = cache.get_doc_encoding(pyesdoc.ESDOC_ENCODING_JSON)

    # Derive ontology.
    ontology = get_doc_ontology(doc)
    if ontology is None:
        rt.raise_error("Ontology {0} is unsupported".format(doc.__class__.type_key))

    # Create document repository.
    document = create_doc(doc, project, None, institute)

    # Create document representation.
    create_doc_representation(document, ontology, encoding, language, doc_json)

    # Create document summary.
    create_doc_summary(document, language)

    # Create document external ID (i.e. simulation id).
    create_doc_external_ids(document)

    # Persist.
    session.commit()

    # Log.
    rt.log("CREATED DOC :: T={0} ID={1} UID={2} V={3}.".format(
        document.Type, document.ID, document.UID, document.Version))

    return {
        id : document.ID
    }


def create_doc(doc, project, endpoint, institute=None):
    """Creates & returns a models.Document instance.

    :param doc: pyesdoc document object representation.
    :type doc: object
    
    :param project: Project with which document is associated.
    :type project: esdoc_api.models.Project

    :param endpoint: Endpoint from which document was ingested.
    :type endpoint: esdoc_api.models.IngestEndpoint

    :param institute: Institute with which document is associated.
    :type institute: esdoc_api.models.Institute

    :returns: A document.
    :rtype: esdoc_api.models.Document

    """
    # Defensive programming.
    rt.assert_doc('doc', doc)
    rt.assert_var('project', project, models.Project)
    rt.assert_optional_var('endpoint', endpoint, models.IngestEndpoint)
    rt.assert_optional_var('institute', institute, models.Institute)

    # Instantiate & assign attributes.
    instance = dao.get_document(project.ID,
                                str(doc.doc_info.id),
                                str(doc.doc_info.version))
    if instance is None:
        instance = create(models.Document)
        instance.as_obj = doc
        if endpoint is not None:
            instance.IngestEndpoint_ID = endpoint.ID
        if institute is not None:
            instance.Institute_ID = institute.ID
        instance.Name = get_doc_name(doc)
        instance.Project_ID = project.ID
        instance.Type = doc.type_key
        instance.UID = str(doc.doc_info.id)
        instance.Version = int(doc.doc_info.version)
        set_doc_is_latest_flag(instance)

    return instance


def create_sub_doc(parent, child):
    """Creates & returns a models.DocumentSubDocument instance.

    :param parent: Parent document.
    :type parent: esdoc_api.models.Document

    :param child: Child document.
    :type child: esdoc_api.models.Document

    :returns: Submodels.Document instance.
    :rtype: esdoc_api.models.DocumentSubDocument

    """
    # Defensive programming.
    rt.assert_var('parent', parent, models.Document)
    rt.assert_var('child', child, models.Document)

    # Ensure parent's sub-document collection is upto date.
    if child not in parent.children:
        parent.children.append(child)

    # Instantiate & assign attributes.
    instance = dao.get_document_sub_document(parent.ID, child.ID)
    if instance is None:
        instance = create(models.DocumentSubDocument)
        instance.Document_ID = parent.ID
        instance.SubDocument_ID = child.ID
        parent.HasChildren = True

    return instance


def set_doc_is_latest_flag(document):
    """Sets flag indicating whether a document is the latest version or not.

    :param document: models.Document whose is_latest flag is being assigned.
    :type document: esdoc_api.models.Document

    """    
    # Defensive programming.
    rt.assert_var('document', document, models.Document)

    # Get all related documents and update IsLatest flag accordingly.
    all = dao.get_document(document.Project_ID, document.UID, models.DOCUMENT_VERSION_ALL)
    for i in range(len(all)):
        all[i].IsLatest = (i == 0)
        if all[i].Version == document.Version:
            document.IsLatest == all[i].IsLatest


def create_doc_drs(document, keys):
    """Factory method to create and return a models.DocumentDRS instance.

    :param document: A deserialized models.Document instance.
    :type document: esdoc_api.models.Document

    :param keys: Set of DRS keys.
    :type keys: list

    :returns: A models.DocumentDRS instance.
    :rtype: esdoc_api.models.DocumentDRS

    """
    # Defensive programming.
    rt.assert_var('document', document, models.Document)
    rt.assert_typed_iter(keys, str)

    # Reformat path.
    path = _DRS_SPLIT.join(keys).upper()

    # Create (only if necessary).
    instance = dao.get_document_drs(document.Project_ID, document.ID, path)
    if instance is None:
        instance = create(models.DocumentDRS)
        instance.Document_ID = document.ID
        instance.Path = path
        instance.Project_ID = document.Project_ID
        for i in range(len(keys)):
            if i > 7:
                break;
            elif keys[i] is not None:
                setattr(instance, "Key_0" + str(i + 1), keys[i].upper())

    return instance


def create_doc_external_ids(document, first_only=False):
    """Factory method to create and return a list of models.DocumentExternalID instances.

    :param document: A deserialized models.Document instance.
    :type document: esdoc_api.models.Document

    :param first_only: Flag indicating whether only the first external id will be returned.
    :type first_only: bool

    :returns: A models.DocumentExternalID instance.
    :rtype: esdoc_api.models.DocumentExternalID

    """
    # Defensive programming.
    rt.assert_var('document', document, models.Document)
    rt.assert_var('first_only', first_only, bool)
    rt.assert_doc('document.as_obj', document.as_obj)

    for id in document.as_obj.doc_info.external_ids:
        instance = dao.get_document_external_id(document.Project_ID,
                                                document.ID,
                                                id.value.upper())
        if instance is None:
            instance = create(models.DocumentExternalID)
            instance.Project_ID = document.Project_ID
            instance.Document_ID = document.ID
            instance.ExternalID = id.value.upper()
        if first_only:
            break

    return dao.get_document_external_ids(document.ID, document.Project_ID)


def create_doc_summary(document, language):
    """Factory method to create and return a models.DocumentSummary instance.

    :param document: A deserialized models.Document instance.
    :type document: esdoc_api.models.Document

    :param language: A models.DocumentLanguage instance.
    :type language: esdoc_api.models.DocumentLanguage

    :returns: A models.DocumentSummary instance.
    :rtype: esdoc_api.models.DocumentSummary

    """
    # Defensive programming.
    rt.assert_var('document', document, models.Document)
    rt.assert_var('language', language, models.DocumentLanguage)

    # Create.
    instance = dao.get_document_summary(document.ID, language.ID)
    if instance is None:
        instance = create(models.DocumentSummary)
        instance.Document_ID = document.ID
        instance.Language_ID = language.ID

    # Set attributes derived from pyesdoc document.
    set_doc_summary(document.as_obj, instance)

    # Rebuild collection.
    document.Summaries = [s for s in document.Summaries if s.ID != instance.ID]
    document.Summaries.append(instance)
    
    return instance


def delete_doc(uid, version):
    """Deletes a document.

    :param uid: Document unique identifier.
    :type uid: str

    :param version: Document version.
    :type version: str

    """
    docs = dao.get_document(None, uid, version)
    if docs is None:
        return
    
    if not rt.is_iterable(docs):
        docs = [docs]

    for doc in docs:
        dao.delete_document(doc.ID)

    # Persist.
    session.commit()


def _get_doc_info(doc, getters):
    # Defensive programming.
    rt.assert_doc('doc', doc)

    # Assign getter.
    getter = None if doc.type_key not in getters else getters[doc.type_key]

    return None if getter is None else getter(doc)


def get_doc_name(doc):
    """Gets document name.

    :param doc: pyesdoc document object representation.
    :type doc: object

    """
    # Defensive programming.
    rt.assert_doc('doc', doc)

    return _get_doc_info(doc, _get_cim_v1_doc_name_getters())


def get_doc_description(doc):
    """Returns document descriptions.

    :param doc: pyesdoc document object representation.
    :type doc: object

    """
    # Defensive programming.
    rt.assert_doc('doc', doc)

    return _get_doc_info(doc, _get_cim_v1_doc_description_getters())


def get_doc_summary_fields(doc):
    """Returns document summary fields.

    :param doc: pyesdoc document object representation.
    :type doc: object

    """
    # Defensive programming.
    rt.assert_doc('doc', doc)
    
    return _get_doc_info(doc, _get_cim_v1_doc_summary_field_getters())


def get_doc_ontology(doc):
    """Returns document ontology.

    :param doc: pyesdoc document object representation.
    :type doc: object

    :returns: pyesdoc document ontology.
    :rtype: models.DocumentOntology

    """
    # Defensive programming.
    rt.assert_doc('doc', doc)

    # Unpack type key.
    o, v, p, t = doc.__class__.type_key.split(".")

    return cache.get_doc_ontology(o, v)


def set_doc_summary(doc, summary):
    """Sets document summary fields.

    :param doc: pyesdoc document object representation.
    :type doc: object

    :param summary: Summary whose fields are being assigned.
    :type summary: esdoc_api.models.DocumentSummary

    """
    # Defensive programming.
    rt.assert_doc('doc', doc)
    rt.assert_var('summary', summary, models.DocumentSummary)

    summary.Description = get_doc_description(doc)
    for i, field in enumerate(get_doc_summary_fields(doc)):
        setattr(summary, 'Field_0' + str(i + 1), str(field))


def create_facet_relation(frt, from_facet, to_facet):
    """Creates a facet relation (if necessary).

    :param frt: models.Facet relation type.
    :type frt: esdoc_api.models.FacetRelationType

    :param from_facet: From facet.
    :type from_facet: esdoc_api.models.Facet

    :param to_facet: To facet.
    :type to_facet: esdoc_api.models.Facet

    """
    # Defensive programming.
    rt.assert_var('frt', frt, models.FacetRelationType)
    rt.assert_var('from_facet', from_facet, models.Facet)
    rt.assert_var('to_facet', to_facet, models.Facet)

    fr = dao.get_facet_relation(frt.ID, from_facet.ID, to_facet.ID)
    if fr is None:
        fr = create(models.FacetRelation)
        fr.Type_ID = frt.ID
        fr.From_ID = from_facet.ID
        fr.To_ID = to_facet.ID
        
    return fr


def create_facet(ft, key, value, value_for_display=None, key_for_sort=None):
    """Creates a facet (if necessary).

    :param ft: models.Facet type.
    :type ft: esdoc_api.models.FacetType

    :param key: models.Facet key.
    :type key: str

    :param key_for_sort: models.Facet sort key.
    :type key_for_sort: str

    :param value: models.Facet value.
    :type value: str

    :param value_for_display: models.Facet display value.
    :type value_for_display: str

    :returns: A facet instance.
    :rtype: esdoc_api.models.Facet

    """
    # Defensive programming.
    rt.assert_var('ft', ft, models.FacetType)
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
        f = create(models.Facet)
        f.Type_ID = ft.ID
        f.Key = key[:2047]
        f.Value = value[:2047]
        if value_for_display is not None:
            f.ValueForDisplay = value_for_display[:2047]
        if key_for_sort is not None:
            f.KeyForSort = key_for_sort[:2047]
        ft.Values.append(f)

    return f


def create_doc_representation(document, 
                                   ontology,
                                   encoding,
                                   language,
                                   representation):
    """Factory method to create a document representation.

    :param document: The document to which a representation is being assigned.
    :type document: esdoc_api.models.Document

    :param ontology: models.Document ontology.
    :type ontology: esdoc_api.models.DocumentOntology

    :param encoding: models.Document representation encoding.
    :type encoding: esdoc_api.models.DocumentEncoding

    :param language: models.Document representation language.
    :type language: esdoc_api.models.DocumentLanguage

    :param representation: models.Document representation, e.g. json | xml.
    :type representation: unicode

    :returns: A document representation.
    :rtype: esdoc_api.models.DocumentRepresentation

    """
    # Defensive programming.
    rt.assert_var('document', document, models.Document)
    rt.assert_var('ontology', ontology, models.DocumentOntology)
    rt.assert_var('encoding', encoding, models.DocumentEncoding)
    rt.assert_var('language', language, models.DocumentLanguage)
    rt.assert_var('representation', representation, unicode)

    # Update or create as appropriate.
    instance = dao.get_doc_reprensentation(document.ID,
                                               ontology.ID,
                                               encoding.ID,
                                               language.ID)
    if instance is None:
        instance = create(models.DocumentRepresentation)
        instance.Document_ID = document.ID
        instance.Ontology_ID = ontology.ID
        instance.Encoding_ID = encoding.ID
        instance.Language_ID = language.ID
    instance.Representation = representation

    return instance


def get_doc_reprensentation(document, ontology, encoding, language):
    """Loads a document representation.

    :param document: A document for which a representation is being retrieved.
    :type document: esdoc_api.models.Document

    :param ontology: models.Document ontology.
    :type ontology: esdoc_api.models.DocumentOntology

    :param encoding: Associated document encoding.
    :type encoding: esdoc_api.models.DocumentEncoding

    :param language: Associated document language.
    :type language: esdoc_api.models.DocumentLanguage

    :returns: A document representation.
    :rtype: esdoc_api.models.DocumentRepresentation

    """
    # Defensive programming.
    rt.assert_var('document', document, models.Document)
    rt.assert_var('ontology', ontology, models.DocumentOntology)
    rt.assert_var('encoding', encoding, models.DocumentEncoding)
    rt.assert_var('language', language, models.DocumentLanguage)

    instance = dao.get_doc_reprensentation(document.ID,
                                               ontology.ID,
                                               encoding.ID,
                                               language.ID)

    return None if instance is None else instance.Representation


def get_facets(type_name):
    """Maps a a list of models.Facet instances by their models.FacetType name to list of lists.

    :param type_name: Name of a models.FacetType.
    :type type_name: str

    :returns: List of models.Facet instances with matching models.FacetType name.
    :rtype: list

    """
    result = []

    ft = dao.get_by_name(models.FacetType, type_name)
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
    """Maps a a list of models.FacetRelation instances by their models.FacetRelationType name to list of lists.

    :param type_name: Name of a models.FacetRelationType.
    :type type_name: str

    :returns: List of models.FacetRelation instances with matching models.FacetRelationType name.
    :rtype: list

    """
    result = []

    frt = dao.get_by_name(models.FacetRelationType, type_name)
    if frt is not None:
        for r in frt.Relations:
            result.append([r.From_ID, r.To_ID])

    return sorted(result, key=lambda r: r[0])


def get_doc_by_obj(project_id, as_obj):
    """Returns a models.Document instance by it's project and pyesdoc object representation.

    :param project_id: ID of a models.Project instance.
    :type project_id: int

    :param as_obj: pyesdoc document object representation.
    :type as_obj: object

    :returns: First matching document.
    :rtype: esdoc_api.models.Document

    """
    # Retrieve.
    doc_info = as_obj.doc_info
    instance = dao.get_document(project_id, doc_info.id, doc_info.version)

    # Assign.
    if instance is not None:
        instance.as_obj = as_obj

    return instance


def _get_cim_v1_doc_summary_field_getters():
    """Returns a tuple of document summary field getters for cim v1.

    """
    def _default(d):
        return (
            d.short_name,
            d.long_name
        )

    def _quality(d):
        return (
            d.doc_info.id,
            d.doc_info.version,
            None if not len(d.doc_info.external_ids) else \
                    d.doc_info.external_ids[0].value
        )

    def _data_object(d):
        return (
            d.acronym,
            d.description
        )

    def _grid_spec(d):
        if len(d.esm_model_grids) > 0:
            return (
                d.esm_model_grids[0].short_name,
                d.esm_model_grids[0].long_name
            )

    def _model_component(d):
        return (
            d.short_name,
            d.long_name,
            None if d.release_date is None else str(d.release_date)
        )

    # Return setter functions organised by document type.
    return {
        cim_v1.TYPE_KEY_DATA_OBJECT : _data_object,
        cim_v1.TYPE_KEY_ENSEMBLE : _default,
        cim_v1.TYPE_KEY_GRID_SPEC : _grid_spec,
        cim_v1.TYPE_KEY_MODEL_COMPONENT : _model_component,
        cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT : _default,
        cim_v1.TYPE_KEY_PLATFORM : _default,
        cim_v1.TYPE_KEY_QUALITY : _quality,
        cim_v1.TYPE_KEY_SIMULATION_RUN : _default,
        cim_v1.TYPE_KEY_STATISTICAL_MODEL_COMPONENT : _model_component
    }


def _get_cim_v1_doc_description_getters():
    """Returns document description getters for cim v1.

    """
    def _default(d):
        return None if d.description is None else d.description[:1023]

    # Return setter functions organised by document type.
    return {
        cim_v1.TYPE_KEY_MODEL_COMPONENT : _default,
        cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT : _default,
        cim_v1.TYPE_KEY_STATISTICAL_MODEL_COMPONENT : _default
    }
    

def _get_cim_v1_doc_name_getters():
    """Returns document name getters for cim v1.

    """
    # Default name setter.
    def _default(d):
        return d.short_name

    # Custom name setters.
    def _data_object(d):
        return d.acronym

    def _grid_spec(d):
        if len(d.esm_model_grids) > 0:
            return d.esm_model_grids[0].short_name
        return None

    def _quality(d):
        if len(d.reports) > 0 and \
           d.reports[0].measure is not None:
            return d.reports[0].measure.name
        return None

    # Getter functions organised by document type.
    return {
        cim_v1.TYPE_KEY_DATA_OBJECT : _data_object,
        cim_v1.TYPE_KEY_ENSEMBLE : _default,
        cim_v1.TYPE_KEY_GRID_SPEC : _grid_spec,
        cim_v1.TYPE_KEY_MODEL_COMPONENT : _default,
        cim_v1.TYPE_KEY_NUMERICAL_EXPERIMENT : _default,
        cim_v1.TYPE_KEY_PLATFORM : _default,
        cim_v1.TYPE_KEY_QUALITY : _quality,
        cim_v1.TYPE_KEY_SIMULATION_RUN : _default,
        cim_v1.TYPE_KEY_STATISTICAL_MODEL_COMPONENT : _default
    }
