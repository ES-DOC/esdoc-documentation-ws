"""
An entity within the es-doc api system.
"""

# Module imports.
import datetime
from operator import add
from functools import reduce

from elixir import *
from sqlalchemy import desc
from sqlalchemy import UniqueConstraint
import uuid

from esdoc_api.models.core.entity_base import *
from esdoc_api.lib.pycim.cim_constants import *
from esdoc_api.lib.pycim.cim_serializer import encode as encode_cim

# Module exports.
__all__ = ['Document']



class Document(CIMEntity):
    """
    A cim document.
    """
    # Elixir directives.
    using_options(tablename='tblDocument')
    using_table_options(UniqueConstraint('Project_ID' ,'UID', 'Version'),
                        schema=DB_SCHEMA_DOCS)

    # Relation set.
    Project = ManyToOne('Project', required=True)
    Institute = ManyToOne('Institute')
    IngestEndpoint = ManyToOne('IngestEndpoint', required=True, lazy=None)
    ExternalIDs = OneToMany('DocumentByExternalID', lazy=None)
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
        self.pycim_doc = None
        

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
        from esdoc_api.models.entities.document_sub_document import DocumentSubDocument

        self.children.append(child)
        DocumentSubDocument.create(self, child)


    def is_match(self, document):
        """Determines whether passed document matches this one.

        Keyword Arguments:
        document - a docuemtn being processed.

        """
        from esdoc_api.models.entities.document import Document

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
        from esdoc_api.models.entities.project import Project

        # Defensive programming.
        if isinstance(document, Document) == False:
            raise TypeError('document')
        if isinstance(project, Project) == False:
            raise TypeError('project')

        # Retrieve latest.
        latest = cls.retrieve_by_id(project, document.UID)

        # Update flags when necessary.
        if latest is None or document.Version >= latest.Version:
            document.IsLatest = True
            if latest is not None and latest.ID != document.ID:
                latest.IsLatest = False


    @classmethod
    def retrieve(cls, project, pycim_doc):
        """Retrieves a single document.

        Keyword Arguments:
        project - a project instance.
        pycim_doc - pycim object representation of document.

        """
        from esdoc_api.models.entities.project import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if pycim_doc is None:
            raise ValueError('pycim_doc')

        # Retrieve.
        instance = cls.retrieve_by_id(project,
                                      pycim_doc.cim_info.id,
                                      pycim_doc.cim_info.version)

        # Assign.
        if instance is not None:
            instance.pycim_doc = pycim_doc

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

        from esdoc_api.models.entities.document_sub_document import DocumentSubDocument

        children = []

        for sub_document in DocumentSubDocument.retrieve(parent):
            children.append(sub_document.Child)

        return children
    

    @classmethod
    def retrieve_by_id(cls, project, uid, version=None):
        """Retrieves a single document.

        Keyword Arguments:
        project - a project instance.
        uid - document identifier.
        version - document version.

        """
        from esdoc_api.models.entities.project import Project

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if uid is None:
            raise ValueError('document uid must be a universal identifier')

        # Set query.
        q = cls.query
        q = q.filter(cls.Project_ID==project.ID)
        q = q.filter(cls.UID==str(uid))
        if version is None:
            q = q.order_by(cls.Version.desc())
        else:
            q = q.filter(cls.Version==int(version))

        # Return first.
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
        from esdoc_api.models.entities.institute import Institute
        from esdoc_api.models.entities.project import Project

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
        from esdoc_api.models.entities.project import Project
        from esdoc_api.models.entities.document_by_drs import DocumentByDRS

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')

        # Get document via querying drs index table.
        instance = DocumentByDRS.retrieve_by_keys(project, key_01, key_02, key_03, key_04, key_05, key_06, key_07, key_08, latest_only)

        return None if instance is None else instance.Document

    
    @classmethod
    def retrieve_by_external_id(cls, project, external_id):
        """Retrieves a document by searching by external id.

        Keyword Arguments:
        project - project with which document is associated.
        external_id - document external identifier.

        """
        from esdoc_api.models.entities.project import Project
        from esdoc_api.models.entities.document_by_external_id import DocumentByExternalID

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if external_id is None:
            raise ValueError('external_id')

        # Get document via querying external identifier index table.
        collection = DocumentByExternalID.retrieve(project, external_id)

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
            return document.pycim_doc.short_name

        def _for_1_5_data_object():
            return document.pycim_doc.acronym

        def _for_1_5_grid_spec():
            if len(document.pycim_doc.esm_model_grids) > 0:
                return document.pycim_doc.esm_model_grids[0].short_name
            return None

        def _for_1_5_quality():
            if len(document.pycim_doc.reports) > 0 and \
               document.pycim_doc.reports[0].measure is not None:
                return document.pycim_doc.reports[0].measure.name
            return None

        # Collection of setter functions organised by document type.
        setters = {
            '1.5' : {
                'dataObject' : _for_1_5_data_object,
                'ensemble' : _default,
                'gridSpec' : _for_1_5_grid_spec,
                'modelComponent' : _default,
                'numericalExperiment' : _default,
                'simulationRun' : _default,
                'platform' : _default,
                'cIM_Quality' : _for_1_5_quality,
            }
        }

        name = None

        # Derive name from setter function.
        schema = document.pycim_doc.cim_info.type_info.schema
        type = document.pycim_doc.cim_info.type_info.type
        if schema in setters and type in setters[schema]:
            name = setters[schema][type]()
            if name is not None:
                name = name.strip().upper()

        return name


    @classmethod
    def create(cls, project, endpoint, pycim_doc):
        """Factory method to create and return an instance.

        Keyword Arguments:

        project - project with which document is associated.
        endpoint - endpoint with which document is associated.
        pycim_doc - pycim object representation of document.

        """
        from esdoc_api.models.entities.project import Project
        from esdoc_api.models.entities.ingest_endpoint import IngestEndpoint

        # Defensive programming.
        if isinstance(project, Project) == False:
            raise TypeError('project')
        if isinstance(endpoint, IngestEndpoint) == False:
            raise TypeError('endpoint')
        if pycim_doc is None:
            raise ValueError('pycim_doc')

        # Instantiate & assign attributes.
        instance = cls()
        instance.pycim_doc = pycim_doc
        instance.Project_ID = project.ID
        instance.IngestEndpoint_ID = endpoint.ID
        instance.UID = str(pycim_doc.cim_info.id)
        instance.Version = int(pycim_doc.cim_info.version)
        instance.Type = pycim_doc.cim_info.type_info.type.upper()
        instance.Name = cls.get_name(instance)
        cls.set_is_latest(instance, project)

        return instance

