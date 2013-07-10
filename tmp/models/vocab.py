"""
.. module:: esdoc_api.lib.repo.models.vocab.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: The controlled vocabulary set of ES-DOC API models.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from sqlalchemy import UniqueConstraint
from elixir import *

from esdoc_api.lib.pyesdoc.utils.ontologies import *
from esdoc_api.lib.repo.models.utils import *


# Module exports.
__all__ = [
    'DocumentEncoding',
    'DocumentLanguage',
    'DocumentOntology',
    'DocumentType',
    'EXECUTION_STATE_QUEUED',
    'EXECUTION_STATE_RUNNING',
    'EXECUTION_STATE_SUSPENDED',
    'EXECUTION_STATE_COMPLETE',
    'EXECUTION_STATE_ERROR',
    'IngestState',
    'Institute',
    'Project'
]


# Constants pertaining to states.
EXECUTION_STATE_QUEUED = u"QUEUED"
EXECUTION_STATE_RUNNING = u"RUNNING"
EXECUTION_STATE_SUSPENDED = u"SUSPENDED"
EXECUTION_STATE_COMPLETE = u"COMPLETE"
EXECUTION_STATE_ERROR = u"ERROR"



# Domain model partition.
_DOMAIN_PARTITION = 'vocab'


class DocumentEncoding(ESDOCEntity):
    """An encoding with which a document representation maybe associated.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentEncoding')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Field set.
    Encoding = Field(Unicode(15), required=True, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Encoding


class DocumentLanguage(ESDOCEntity):
    """A language with which a document is associated.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentLanguage')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Field set.
    Code = Field(Unicode(2), required=True)
    Name =  Field(Unicode(127), required=True, unique=True)


    @property
    def FullName(self):
        """
        Gets the full institute name derived by concatanation.
        """
        return self.Code + u" - " + self.Name


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Code


    @classmethod
    def retrieve(cls, code=ESDOC_DEFAULT_LANGUAGE):
        """Gets an instance of the entity by code.

        Keyword Arguments:
        code - language code.

        """
        # Defensive programming.
        if isinstance(code, str) == False and isinstance(code, unicode) == False:
            raise TypeError('code')

        return cls.get_by(Code=code.lower())


class DocumentOntology(ESDOCEntity):
    """An ontology with which a document is associated.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentOntology')
    using_table_options(UniqueConstraint('Name', 'Version'),
                        schema=_DOMAIN_PARTITION)


    # Field set.
    Name = Field(Unicode(63), required=True)
    Version = Field(Unicode(31), required=True)


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.

        """
        return lambda instance: instance.Name + instance.Version


    @classmethod
    def retrieve(cls, name, version):
        """Returns a document ontology entity.

        :param name: Ontology name.
        :type name: str

        :param version: Ontology version.
        :type version: str

        :returns: Document ontology entity instance.
        :rtype: esdoc_api.lib.repo.models.document_ontology.DocumentOntology

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')
        if version is None:
            raise ValueError('version')

        # Set query.
        q = cls.query
        q = q.filter(cls.Name==name)
        q = q.filter(cls.Version==version)

        # Return first.
        return q.first()


class DocumentType(ESDOCEntity):
    """Meta-information regarding the type of document.

    """
    # Elixir directives.
    using_options(tablename='tblDocumentType')
    using_table_options(UniqueConstraint('Ontology_ID' ,'Package', 'Name'),
                        UniqueConstraint('Ontology_ID' ,'ShortName'),
                        schema=_DOMAIN_PARTITION)

    # Relation set.
    Ontology = ManyToOne('DocumentOntology', required=True)

    # Field set.
    Package = Field(Unicode(63), required=True)
    Name = Field(Unicode(63), required=True)
    ShortName = Field(Unicode(31), required=True)
    DisplayName = Field(Unicode(63), required=True)


    def full_name(self):
        result = self.Ontology.Name
        result += '-v'
        result = self.Ontology.Version
        result += '.'
        result = self.Package.strip().lower()
        result += '.'
        result = self.Name.strip().lower()
        return result


    @classmethod
    def get_default_sort_key(cls):
        """Gets default sort key.

        """
        return lambda instance: instance.full_name


class IngestState(ESDOCEntity):
    """The state that a ingest process may be in, i.e. InProgress, Queued, Error...etc.
    
    """
    # Elixir directives.
    using_options(tablename='tblIngestState')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Field set.
    Name =  Field(Unicode(16), required=True, unique=True)
    Description =  Field(Unicode(128), required=True)
    Code =  Field(Integer, required=True, unique=True)


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Code


    @classmethod
    def get_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of ingest state.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name)


class Institute(ESDOCEntity):
    """Represents an institute with which documents are associated.

    """
    # Elixir directives.
    using_options(tablename='tblInstitute')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Field set.
    Name =  Field(Unicode(16), required=True, unique=True)
    Synonym =  Field(Unicode(16), required=False, unique=True)
    LongName =  Field(Unicode(512), required=True)
    CountryCode = Field(Unicode(2), required=True)
    URL =  Field(Unicode(256))


    @property
    def FullName(self):
        """Gets the full institute name derived by concatanation.

        """
        return self.CountryCode + u" - " + self.Name + u" - " + self.LongName


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.FullName


    @classmethod
    def get_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of institute.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name)


    @classmethod
    def retrieve_by_name(cls, name):
        """Gets an instance of the entity by name.

        Keyword Arguments:
        name - name of institute.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name)


class Project(ESDOCEntity):
    """Represents a project with which documents are associated.

    """
    # Elixir directives.
    using_options(tablename='tblProject')
    using_table_options(schema=_DOMAIN_PARTITION)

    # Field set.
    Name =  Field(Unicode(16), required=True, unique=True)
    Description =  Field(Unicode(1023))
    URL =  Field(Unicode(1023))


    @classmethod
    def get_default_sort_key(cls):
        """
        Gets default sort key.
        """
        return lambda instance: instance.Name


    @classmethod
    def retrieve(cls, name):
        """Gets an instance of the entity by code.

        Keyword Arguments:
        name - project name.

        """
        # Defensive programming.
        if name is None:
            raise ValueError('name')

        return cls.get_by(Name=name.upper())
