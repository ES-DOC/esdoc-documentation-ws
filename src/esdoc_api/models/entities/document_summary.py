"""
An entity within the es-doc api system.
"""

# Module imports.
from operator import add

from sqlalchemy import UniqueConstraint

from esdoc_api.models.core.entity_base import *
from esdoc_api.lib.pycim.cim_constants import *

# Module exports.
__all__ = ['DocumentSummary']



class DocumentSummary(CIMEntity):
    """
    Summary information pertaining to a cim document.
    """
    # Elixir directives.
    using_options(tablename='tblDocumentSummary')
    using_table_options(UniqueConstraint('Document_ID', 'Language_ID'),
                        schema=DB_SCHEMA_DOCS)

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

        def _for_1_5_cim_quality():
            if len(obj.cim_info.external_ids) > 0:
                self.Field_01 = obj.cim_info.external_ids[0].value
            else:
                self.Field_02 = str(obj.cim_info.id)
            self.Field_02 = str(obj.cim_info.version)

        def _for_1_5_data_object():
            self.Field_01 = obj.acronym
            self.Field_02 = obj.description

        def _for_1_5_grid_spec():
            if len(obj.esm_model_grids) > 0:                
                self.Field_01 = obj.esm_model_grids[0].short_name
                self.Field_02 = obj.esm_model_grids[0].long_name

        def _for_1_5_model_component():
            self.Field_01 = obj.short_name
            self.Field_02 = obj.long_name
            if obj.release_date is not None:
                self.Field_03 = str(obj.release_date)

        # Collection of setter functions organised by cim document type.
        setters = {
            '1.5' : {
                'cIM_Quality' : _for_1_5_cim_quality,
                'dataObject' : _for_1_5_data_object,
                'ensemble' : _for_default,
                'gridSpec' : _for_1_5_grid_spec,
                'modelComponent' : _for_1_5_model_component,
                'numericalExperiment' : _for_default,
                'simulationRun' : _for_default,
                'platform' : _for_default,
            }
        }

        # Derive setter.
        schema = obj.cim_info.type_info.schema
        type = obj.cim_info.type_info.type
        setter = setters[schema][type]

        # Invoke setter.
        if setter is not None:
            setter()


    @classmethod
    def remove_all(cls, document):
        """Deletes collection by document.

        Keyword Arguments:
        document - document being deleted.

        """
        from esdoc_api.models.entities.document import Document

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
        from esdoc_api.models.entities.document import Document
        from esdoc_api.models.entities.document_language import DocumentLanguage

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
        from esdoc_api.models.entities.document import Document

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
        from esdoc_api.models.entities.document import Document
        from esdoc_api.models.entities.document_language import DocumentLanguage

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
        from esdoc_api.models.entities.document import Document
        from esdoc_api.models.entities.document_language import DocumentLanguage

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
            instance.set_fields(document.pycim_doc)
            
        return instance

