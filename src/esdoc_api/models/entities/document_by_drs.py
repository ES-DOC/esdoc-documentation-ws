"""
An entity within the es-doc api system.
"""

# Module imports.
from elixir import *
from sqlalchemy import UniqueConstraint

from symbol import for_stmt
from esdoc_api.models.core.entity_base import *


# Module exports.
__all__ = ['DocumentByDRS']


# Default drs split.
_DRS_SPLIT = '/'


class DocumentByDRS(CIMEntity):
    """A cim document drs indexing table.
    
    """
    # Elixir directives.
    using_options(tablename='tblDocumentByDRS')
    using_table_options(UniqueConstraint('Project_ID' ,'Document_ID', 'Path'),
                        schema=DB_SCHEMA_DOCS)

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
        result = DocumentByDRS()

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
        :rtype: esdoc_api.models.entities.DocumentByDRS
        
        """
        from esdoc_api.models.entities.document import Document

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
        from esdoc_api.models.entities.document import Document

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
        from esdoc_api.models.entities.project import Project
        from esdoc_api.models.entities.document import Document

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

