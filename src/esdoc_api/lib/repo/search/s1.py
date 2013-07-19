"""Encapsulate a prodiguer data node search.

"""

# Module imports.
from datetime import datetime as dt

from esdoc_api.lib.repo.search.utils import (
    ESDOCSearchBase,
    ESDOCSearchCriteriaBase
    )
from esdoc_api.models import (
    Document,
    DocumentLanguage,
    DocumentSummary,
    Institute,
    Project
    )
from esdoc_api.lib.pyesdoc.utils.ontologies import *




class S1Search(ESDOCSearchBase):
    """Encapsulates a basic search over esdoc repository.

    """

    def __init__(self):
        """
        Constructor.
        """
        super(S1Search,self).__init__(S1SearchCriteria)


    def format_results(self, results):
        """Formats search results.

        :param results: Set of search results.
        :type results: list

        """   
        def format(r):
            return {
                'documentName' : r.Document.Name,
                'documentType' : r.Document.Type,
                'documentUID' : r.Document.UID,
                'documentVersion' : r.Document.Version,
                'project' : r.Document.Project.Name,
                'institute' : None if r.Document.Institute is None else r.Document.Institute.Name,
                'field01' : r.Field_01,
                'field02' : r.Field_02,
                'field03' : r.Field_03,
                'field04' : r.Field_04,
                'field05' : r.Field_05,
                'field06' : r.Field_06,
                'field07' : r.Field_07,
                'field08' : r.Field_08                   
            }

        return map(format, results)
    

    def set_query(self, ctx):
        """Sets sqlalchemy query object used to drive search process.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        # Initialise query.
        ctx.q = DocumentSummary.query
        ctx.q = ctx.q.join(DocumentSummary.Document)


    def set_query_filter(self, ctx):
        """Applies query filters.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        print ctx.c
        
        # institute.
        if ctx.c.institute is not None and \
           ctx.c.institute != '*':
            if isinstance(ctx.c.institute, unicode):
                print 'DSDSDSDSS'
            else:                
                print 'SEARCHING BY :: institute :: {0}'.format(ctx.c.institute)
                ctx.set_filter(Document.Institute_ID==ctx.c.institute)

        # language.
        if ctx.c.language is not None and \
           ctx.c.language != '*':
            print 'SEARCHING BY :: language :: {0}'.format(ctx.c.language)
            ctx.set_filter(DocumentSummary.Language_ID==ctx.c.language)

        # name.
        if ctx.c.name is not None and \
           ctx.c.name != '*':
            print 'SEARCHING BY :: name :: {0}'.format(ctx.c.name)
            ctx.set_filter(Document.Name==ctx.c.name)

        # project.
        if ctx.c.project is not None and \
           ctx.c.project != '*':
            print 'SEARCHING BY :: project :: {0}'.format(ctx.c.project)
            ctx.set_filter(Document.Project_ID==ctx.c.project)

        # type.
        if ctx.c.type is not None and \
           ctx.c.type != '*':
            print 'SEARCHING BY :: type :: {0}'.format(ctx.c.type)
            ctx.set_filter(Document.Type==ctx.c.type)

        # version.
        if ctx.c.version == ESDOC_VERSION_LATEST:
            print 'SEARCHING BY :: version :: {0}'.format(ctx.c.version)
            ctx.set_filter(Document.IsLatest==True)


    def set_query_sort(self, ctx):
        """Applies query sorts.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        pass
        ctx.q.order_by(Document.Type, Document.ID)



class S1SearchCriteria(ESDOCSearchCriteriaBase):
    """Search criteria.

    """
    @property
    def keys(self):
        """Gets list of criteria keys.

        :returns: a list of criteria keys.
        :rtype: string list

        """
        return ['institute', 'language', 'name', 'project', 'type', 'version']


    @property
    def codes(self):
        """Gets list of criteria codes.

        :returns: a list of criteria codes.
        :rtype: code list

        """
        return {
            'institute' : Institute.get_by_name,
            'language' : DocumentLanguage.retrieve,
            'project' : Project.retrieve
        }


    def format_name(self):
        self.name = self.name.upper()


    def format_type(self):
        self.type = self.type.upper()


    def format_version(self):
        if self.version != ESDOC_VERSION_LATEST:
            self.version = None

    

