"""
.. module:: esdoc_api.lib.repo.models.vocab.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The controlled vocabulary set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import datetime
import uuid

from sqlalchemy import UniqueConstraint
from elixir import *

from esdoc_api.lib.pyesdoc.utils.ontologies import *
from esdoc_api.lib.repo.models.utils import ESDOCEntity



# Module exports.
__all__ = [
    'Document',
    'DocumentDRS',
    'DocumentExternalID',
    'DocumentRepresentation',
    'DocumentSubDocument',
    'DocumentSummary',
]



# Domain model partition.
_DOMAIN_PARTITION = 'docs'

# Default drs split.
_DRS_SPLIT = '/'

# Document version related constants.
DOCUMENT_VERSION_LATEST = 'latest'
DOCUMENT_VERSION_ALL = 'all'


class Document(ESDOCEntity):
    """A document ingested into the ES-DOC API repository.
    
    """
    # Elixir directives.
    using_options(tablename='tblDocument')
    using_table_options(UniqueConstraint('Project_ID' ,'UID', 'Version'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Project = ManyToOne('Project', required=True)
    Institute = ManyToOne('Institute')
    IngestEndpoint = ManyToOne('IngestEndpoint', lazy=None)
    ExternalIDs = OneToMany('DocumentExternalID', lazy=None)
    Summaries = OneToMany('DocumentSummary', lazy=None)
    Representations = OneToMany('DocumentRepresentation', lazy=None)

    # Field set.
    Type = Field(Unicode(63), required=True)
    Name =  Field(Unicode(255), required=True)
    UID = Field(Unicode(63), required=True, default=str(uuid.uuid4()))
    Version = Field(Integer, required=True, default=1)
    HasChildren = Field(Boolean, required=True, default=False)
    IsChild = Field(Boolean, required=True, default=False)
    IsLatest = Field(Boolean, required=True, default=False)
    IsIndexed = Field(Boolean, required=True, default=False)
    IngestDate =  Field(DateTime, default=datetime.datetime.now)


    def __init__(self):
        """Constructor.

        """
        super(Document, self).__init__()
        self.children = []
        self.as_obj = None


    @property
    def summary(self):
        """Gets top summary from associated collection.

        """
        if self.Summaries is not None or len(self.Summaries) > 0:
            return self.Summaries[0]
        return None


    def append_child(self, child):
        """Appends a child document.

        Keyword Arguments:
        child - a child document being processed.

        """
        self.children.append(child)
        DocumentSubDocument.create(self, child)


    def is_match(self, document):
        """Determines whether passed document matches this one.

        Keyword Arguments:
        document - a docuemtn being processed.

        """
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')

        return self.UID == document.UID and self.Version == document.Version


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.UID + str(instance.Version)


    @classmethod
    def set_is_latest(cls, document, project):
        """Sets flag indicating whether this document is the latest version or not.

        Keyword Arguments:
        document - a document instance.
        project - a project instance.

        """
        from esdoc_api.lib.repo.models import Project

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if isinstance(project, Project) == False:
            raise TypeError('project')

        # Retrieve latest.
        latest = cls.retrieve_by_id(project, document.UID, DOCUMENT_VERSION_LATEST)

        # Update flags when necessary.
        if latest is None or document.Version >= latest.Version:
            document.IsLatest = True
            if latest is not None and latest.ID != document.ID:
                latest.IsLatest = False


    @classmethod
    def retrieve(cls, project, as_obj):
        """Retrieves a single document.

        Keyword Arguments:
        project - a project instance.
        as_obj - pyesdoc object representation of document.

        """
        from esdoc_api.lib.repo.models import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if as_obj is None:
            raise ValueError('as_obj')

        # Retrieve.
        instance = cls.retrieve_by_id(project,
                                      as_obj.cim_info.id,
                                      as_obj.cim_info.version)

        # Assign.
        if instance is not None:
            instance.as_obj = as_obj

        return instance


    @classmethod
    def retrieve_children(cls, parent):
        """Retrieves child documents.

        Keyword Arguments:
        parent - parent document.

        """
        # Defensive programming.
        if isinstance(parent, cls) == False:
            raise TypeError('parent')

        children = []

        for sub_document in DocumentSubDocument.retrieve(parent):
            children.append(sub_document.Child)

        return children


    @classmethod
    def retrieve_by_id(cls, project, uid, version):
        """Retrieves a single document.

        Keyword Arguments:
        project - a project instance.
        uid - document identifier.
        version - document version.

        """
        from esdoc_api.lib.repo.models import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if uid is None:
            raise ValueError('document uid must be a universal identifier')

        # Set query.
        q = cls.query
        q = q.filter(cls.Project_ID==project.ID)
        q = q.filter(cls.UID==str(uid))
        if version is None or version == 'latest' or version == 'all' or len(version) == 0:
            q = q.order_by(cls.Version.desc())
        else:
            q = q.filter(cls.Version==int(version))

        # Return either all or first.
        if version == 'all':
            return q.all()
        else:
            return q.first()


    @classmethod
    def retrieve_by_name(cls, project, type, name, institute=None, latest_only=True):
        """Retrieves a single document by it's name.

        Keyword Arguments:
        project - project with which document is associated.
        type - document type.
        name - document name.
        institute - Institute name.

        """
        from esdoc_api.lib.repo.models import (
            Institute,
            Project
            )

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if type is None:
            raise ValueError('type')
        if name is None:
            raise ValueError('name')
        if institute is not None and isinstance(institute, Institute) == False:
            raise TypeError('institute')

        # Set query.
        q = cls.query
        q = q.filter(cls.Project_ID==project.ID)
        q = q.filter(cls.Type==type.upper())
        q = q.filter(cls.Name==name.upper())
        if institute is not None:
            q = q.filter(cls.Institute_ID==institute.ID)
        if latest_only == True:
            q = q.filter(cls.IsLatest==True)

        # Return first.
        return q.first()


    @classmethod
    def retrieve_by_drs_keys(cls,
                             project,
                             key_01=None,
                             key_02=None,
                             key_03=None,
                             key_04=None,
                             key_05=None,
                             key_06=None,
                             key_07=None,
                             key_08=None,
                             latest_only = True):
        """Retrieves a single document set from matched drs keys.

        Keyword Arguments:

        :param project: A project instance.
        :param key_01: DRS key 1.
        :param key_02: DRS key 2.
        :param key_03: DRS key 3.
        :param key_04: DRS key 4.
        :param key_05: DRS key 5.
        :param key_06: DRS key 6.
        :param key_07: DRS key 7.
        :param key_08: DRS key 8.
        :type project: str
        :type key_01: str
        :type key_02: str
        :type key_03: str
        :type key_04: str
        :type key_05: str
        :type key_06: str
        :type key_07: str
        :type key_08: str

        :returns: a set of documents.
        :rtype: document list

        """
        from esdoc_api.lib.repo.models import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')

        # Get document via querying drs index table.
        instance = DocumentDRS.retrieve_by_keys(project, key_01, key_02, key_03, key_04, key_05, key_06, key_07, key_08, latest_only)

        return None if instance is None else instance.Document


    @classmethod
    def retrieve_by_external_id(cls, project, external_id):
        """Retrieves a document by searching by external id.

        Keyword Arguments:
        project - project with which document is associated.
        external_id - document external identifier.

        """
        from esdoc_api.lib.repo.models import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if external_id is None:
            raise ValueError('external_id')

        # Get document via querying external identifier index table.
        collection = DocumentExternalID.retrieve(project, external_id)

        result = []
        if collection is not None:
            for instance in collection:
                result.append(instance.Document)
        return result


    @classmethod
    def get_name(cls, document):
        """Gets document name.

        Keyword Arguments:
        document - document bieing processed.

        """
        def _default():
            return document.as_obj.short_name

        def _for_cim_1_data_object():
            return document.as_obj.acronym

        def _for_cim_1_grid_spec():
            if len(document.as_obj.esm_model_grids) > 0:
                return document.as_obj.esm_model_grids[0].short_name
            return None

        def _for_cim_1_quality():
            if len(document.as_obj.reports) > 0 and \
               document.as_obj.reports[0].measure is not None:
                return document.as_obj.reports[0].measure.name
            return None

        # Collection of setter functions organised by document type.
        setters = {
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

        name = None

        # Set type info.
        ontology_name = document.as_obj.cim_info.type_info.ontology_name
        ontology_version = document.as_obj.cim_info.type_info.ontology_version
        type_name = document.as_obj.cim_info.type_info.type

        # Use setter to assign name.
        if ontology_name in setters and \
           ontology_version in setters[ontology_name] and \
           type_name in setters[ontology_name][ontology_version]:
            name = setters[ontology_name][ontology_version][type_name]()
            if name is not None:
                name = name.strip().upper()

        return name


    @classmethod
    def create(cls, project, endpoint, as_obj):
        """Factory method to create and return an instance.

        Keyword Arguments:

        project - project with which document is associated.
        endpoint - endpoint with which document is associated.
        as_obj - pyesdoc object representation of document.

        """
        from esdoc_api.lib.repo.models import (
            Project,
            IngestEndpoint
            )

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if isinstance(endpoint, IngestEndpoint) == False:
            raise TypeError('endpoint')
        if as_obj is None:
            raise ValueError('as_obj')

        # Instantiate & assign attributes.
        instance = cls()
        instance.as_obj = as_obj
        instance.Project_ID = project.ID
        instance.IngestEndpoint_ID = endpoint.ID
        instance.UID = str(as_obj.cim_info.id)
        instance.Version = int(as_obj.cim_info.version)
        instance.Type = as_obj.cim_info.type_info.type.upper()
        instance.Name = cls.get_name(instance)
        cls.set_is_latest(instance, project)

        return instance


class DocumentDRS(ESDOCEntity):
    """Encapsulates information required to resolve a document from DRS (directory reference syntax) info.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentDRS')
    using_table_options(UniqueConstraint('Project_ID' ,'Document_ID', 'Path'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Project = ManyToOne('Project', required=True)
    Document = ManyToOne('Document', required=True)

    # Field set.
    Path = Field(Unicode(511))
    Key_01 = Field(Unicode(63))
    Key_02 = Field(Unicode(63))
    Key_03 = Field(Unicode(63))
    Key_04 = Field(Unicode(63))
    Key_05 = Field(Unicode(63))
    Key_06 = Field(Unicode(63))
    Key_07 = Field(Unicode(63))
    Key_08 = Field(Unicode(63))


    def clone(self):
        """Returns a cloned instance.

        """
        result = DocumentDRS()

        result.Document_ID = self.Document_ID
        result.Key_01 = self.Key_01
        result.Key_02 = self.Key_02
        result.Key_03 = self.Key_03
        result.Key_04 = self.Key_04
        result.Key_05 = self.Key_05
        result.Key_06 = self.Key_06
        result.Key_07 = self.Key_07
        result.Key_08 = self.Key_08
        result.Path = self.Path
        result.Project_ID = self.Project_ID

        return result


    def reset_path(self):
        """Resets drs path based upon value of keys.

        """
        path = ''
        for i in range(8):
            key = getattr(self, "Key_0" + str(i + 1))
            if key is not None:
                if i > 0:
                    path += _DRS_SPLIT
                path += key.upper()
        self.Path = path


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Path


    @classmethod
    def create(cls, document, keys):
        """Factory method to create and return an instance.

        :param document: A deserialized document.
        :param keys: Set of DRS keys.
        :type document: lxml.etree
        :type keys: list
        :returns: An instance.
        :rtype: esdoc_api.lib.repo.models.DocumentDRS

        """
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if keys is None:
            raise ValueError('keys')

        result = None

        # Reformat path.
        path = _DRS_SPLIT.join(keys).upper()

        # Create if necessary.
        result = cls.retrieve_duplicate(document, path)
        if result is None:
            result = cls()
            result.Document_ID = document.ID
            result.Path = path
            result.Project_ID = document.Project_ID
            for i in range(len(keys)):
                if i > 7:
                    break;
                elif keys[i] is not None:
                    setattr(result, "Key_0" + str(i + 1), keys[i])

        return result


    @classmethod
    def retrieve_duplicate(cls, document, path):
        """Retrieves a duplicate instance.

        Keyword Arguments:
        document - a cim document.
        path - drs path.

        """
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if path is None:
            raise ValueError('path')

        # Set query.
        q = cls.query.join(cls.Document)
        q = q.filter(cls.Project_ID==document.Project_ID)
        q = q.filter(cls.Document_ID==document.ID)
        q = q.filter(cls.Path==path)

        # Return first.
        return q.first()


    @classmethod
    def retrieve_by_keys(cls,
                         project,
                         key_01=None,
                         key_02=None,
                         key_03=None,
                         key_04=None,
                         key_05=None,
                         key_06=None,
                         key_07=None,
                         key_08=None,
                         latest_only = True):
        """Retrieves a document by matching against drs keys.

        Keyword Arguments:

        project - project with which document set is associated.
        key_01 - drs key 01.
        key_02 - drs key 02.
        key_03 - drs key 03.
        key_04 - drs key 04.
        key_05 - drs key 05.
        key_06 - drs key 06.
        key_07 - drs key 07.
        key_08 - drs key 08.
        latest_only - flag indicating whether only latest records are to be returned.

        """
        from esdoc_api.lib.repo.models import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')

        # Set query.
        q = cls.query.join(cls.Document)
        q = q.filter(cls.Project_ID==project.ID)
        if key_01 is not None:
            q = q.filter(cls.Key_01==str(key_01).upper())
        if key_02 is not None:
            q = q.filter(cls.Key_02==str(key_02).upper())
        if key_03 is not None:
            q = q.filter(cls.Key_03==str(key_03).upper())
        if key_04 is not None:
            q = q.filter(cls.Key_04==str(key_04).upper())
        if key_05 is not None:
            q = q.filter(cls.Key_05==str(key_05).upper())
        if key_06 is not None:
            q = q.filter(cls.Key_06==str(key_06).upper())
        if key_07 is not None:
            q = q.filter(cls.Key_07==str(key_07).upper())
        if key_08 is not None:
            q = q.filter(cls.Key_08==str(key_08).upper())
        if latest_only == True:
            q = q.filter(Document.IsLatest==True)

        # Return first.
        return q.first()


class DocumentExternalID(ESDOCEntity):
    """The external id of a cim document.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentExternalID')
    using_table_options(UniqueConstraint('Project_ID', 'Document_ID', 'ExternalID'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Project = ManyToOne('Project', required=True)
    Document = ManyToOne('Document', required=True)

    # Field set.
    ExternalID = Field(Unicode(255), required=True)


    @classmethod
    def retrieve(cls, project, external_id, latest_only=True):
        """Retrieves a single instance.

        Keyword Arguments:
        document - a cim document.
        external_id - a cim document.

        """
        from esdoc_api.lib.repo.models import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if external_id is None:
            raise ValueError('external_id')

        # Set query.
        q = cls.query.join(cls.Document)
        q = q.filter(cls.Project_ID==project.ID)
        q = q.filter(cls.ExternalID.like('%' + external_id.upper() + '%'))
        if latest_only == True:
            q = q.filter(Document.IsLatest==True)

        # Return first.
        return q.all()


    @classmethod
    def retrieve_duplicate(cls, document, external_id):
        """Retrieves a duplicate instance.

        Keyword Arguments:
        document - a cim document.
        external_id - a cim document.

        """
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if external_id is None:
            raise ValueError('external_id')

        # Set query.
        q = cls.query.join(cls.Document)
        q = q.filter(cls.Project_ID==document.Project_ID)
        q = q.filter(cls.Document_ID==document.ID)
        q = q.filter(cls.ExternalID==external_id.upper())

        # Return first.
        return q.first()


    @classmethod
    def create(cls, document, first_only=False):
        """Create & returns external id references to cim documents.

        Keyword Arguments:
        document - a cim document.
        first_only - flag indicating whether only the first external id will be imported.

        """
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if document.as_obj is None:
            raise ValueError('document.as_obj')

        collection = []
        for id in document.as_obj.cim_info.external_ids:
            instance = cls.retrieve_duplicate(document, id.value)
            if instance is None:
                instance = cls()
                instance.Project_ID = document.Project_ID
                instance.Document_ID = document.ID
                instance.ExternalID = id.value.upper()
            collection.append(instance)
            if first_only:
                break

        return collection


class DocumentRepresentation(ESDOCEntity):
    """A document representation in one of the supported encodings.
    
    """
    # Elixir directives.
    using_options(tablename='tblDocumentRepresentation')
    using_table_options(UniqueConstraint('Document_ID', 'Ontology_ID',
                                         'Encoding_ID', 'Language_ID'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Document = ManyToOne('Document', required=True)
    Ontology = ManyToOne('DocumentOntology', required=True)
    Encoding = ManyToOne('DocumentEncoding', required=True)
    Language = ManyToOne('DocumentLanguage', required=True)

    # Field set.
    Representation = Field(Text)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Encoding


class DocumentSubDocument(ESDOCEntity):
    """Encapsulates document to sub-document relationship information.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentSubDocument')
    using_table_options(UniqueConstraint('Parent_ID' ,'Child_ID'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Parent = ManyToOne('Document', required=True, lazy=None)
    Child  = ManyToOne('Document', required=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: str(instance.Parent_ID) + " :: " + str(instance.Child_ID)


    @classmethod
    def retrieve(cls, parent):
        """Retrieves a set of instances.

        Keyword Arguments:

        parent - parent document.

        """
        # Defensive programming.
        if isinstance(parent, Document) == False:
            raise TypeError('parent')

        # Set query.
        q = cls.query
        q = q.filter(cls.Parent_ID==parent.ID)

        # Return first.
        return q.all()


    @classmethod
    def retrieve_duplicate(cls, parent, child):
        """Retrieves a duplicate instance.

        Keyword Arguments:

        parent - parent document.
        child - child document.

        """
        # Defensive programming.
        if isinstance(parent, Document) == False:
            raise TypeError('parent')
        if isinstance(child, Document) == False:
            raise TypeError('child')

        # Set query.
        q = cls.query
        q = q.filter(cls.Parent_ID==parent.ID)
        q = q.filter(cls.Child_ID==child.ID)

        # Return first.
        return q.first()


    @classmethod
    def create(cls, parent, child):
        """Factory method to create and return an instance.

        Keyword Arguments:

        parent - parent document.
        child - child document.

        """
        # Defensive programming.
        if isinstance(parent, Document) == False:
            raise TypeError('parent')
        if isinstance(child, Document) == False:
            raise TypeError('child')

        # Instantiate & assign attributes.
        instance = cls.retrieve_duplicate(parent, child)
        if instance is None:
            instance = cls()
            instance.Parent_ID = parent.ID
            instance.Child_ID = child.ID
            parent.HasChildren = True

        return instance



class DocumentSummary(ESDOCEntity):
    """Encapsulates document summary information.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentSummary')
    using_table_options(UniqueConstraint('Document_ID', 'Language_ID'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Document = ManyToOne('Document', required=True)
    Language = ManyToOne('DocumentLanguage', required=True)

    # Field set.
    Field_01 = Field(Unicode(1023))
    Field_02 = Field(Unicode(1023))
    Field_03 = Field(Unicode(1023))
    Field_04 = Field(Unicode(1023))
    Field_05 = Field(Unicode(1023))
    Field_06 = Field(Unicode(1023))
    Field_07 = Field(Unicode(1023))
    Field_08 = Field(Unicode(1023))


    def set_fields(self, obj):
        """Sets summary information for each of the different cim types.

        Keyword Arguments:
        obj - decoded instance of a cim document object.

        """
        def _for_default():
            self.Field_01 = obj.short_name
            self.Field_02 = obj.long_name

        def _for_cim_1_cim_quality():
            if len(obj.cim_info.external_ids) > 0:
                self.Field_01 = obj.cim_info.external_ids[0].value
            else:
                self.Field_02 = str(obj.cim_info.id)
            self.Field_02 = str(obj.cim_info.version)

        def _for_cim_1_data_object():
            self.Field_01 = obj.acronym
            self.Field_02 = obj.description

        def _for_cim_1_grid_spec():
            if len(obj.esm_model_grids) > 0:
                self.Field_01 = obj.esm_model_grids[0].short_name
                self.Field_02 = obj.esm_model_grids[0].long_name

        def _for_cim_1_model_component():
            self.Field_01 = obj.short_name
            self.Field_02 = obj.long_name
            if obj.release_date is not None:
                self.Field_03 = str(obj.release_date)

        # Collection of setter functions organised by cim document type.
        setters = {
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

        # Derive setter.
        ontology_name = obj.cim_info.type_info.ontology_name
        ontology_version = obj.cim_info.type_info.ontology_version
        type_name = obj.cim_info.type_info.type
        setter = setters[ontology_name][ontology_version][type_name]

        # Invoke setter.
        if setter is not None:
            setter()


    @classmethod
    def remove_all(cls, document):
        """Deletes collection by document.

        Keyword Arguments:
        document - document being deleted.

        """
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')

        # Set query.
        q = cls.query
        q = q.filter(cls.Document_ID==document.ID)

        # Delete all.
        for ds in q.all():
            ds.delete()


    @classmethod
    def remove(cls, document, language):
        """Deletes instance by document & language.

        Keyword Arguments:
        document - document being deleted.
        language - associated document language.

        """
        from esdoc_api.lib.repo.models import DocumentLanguage

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if isinstance(language, DocumentLanguage) == False:
            raise TypeError('language')

        # Set query.
        q = cls.query
        q = q.filter(cls.Document_ID==document.ID)
        q = q.filter(cls.Language_ID==language.ID)

        # Delete first.
        ds = q.first()
        if ds is not None:
            ds.delete()


    @classmethod
    def retrieve_all(cls, document):
        """Retrives collection by document.

        Keyword Arguments:
        document - associated document.

        """
        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')

        # Set query.
        q = cls.query
        q = q.filter(cls.Document_ID==document.ID)

        # Return all.
        return q.all()


    @classmethod
    def retrieve(cls, document, language):
        """Retrives instance by document & language.

        Keyword Arguments:
        document - associated document.
        language - associated language.

        """
        from esdoc_api.lib.repo.models import DocumentLanguage

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if isinstance(language, DocumentLanguage) == False:
            raise TypeError('language')

        # Set query.
        q = cls.query
        q = q.filter(cls.Document_ID==document.ID)
        q = q.filter(cls.Language_ID==language.ID)

        # Return first.
        return q.first()


    @classmethod
    def create(cls, document, language):
        """Creates instance from document & deserialized object.

        Keyword Arguments:
        document - a cim document.
        language - cim document language.

        """
        from esdoc_api.lib.repo.models import DocumentLanguage

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if isinstance(language, DocumentLanguage) == False:
            raise TypeError('language')

        instance = cls.retrieve(document, language)
        if instance is None:
            instance = DocumentSummary()
            instance.Document_ID = document.ID
            instance.Language_ID = language.ID
            instance.set_fields(document.as_obj)

        return instance

