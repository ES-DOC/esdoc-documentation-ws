"""
.. module:: esdoc_api.lib.repo.search.utils.py
   :copyright: Copyright "Jun 29, 2013", Earth System Documentation
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Search utility classes / functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
import abc

from esdoc_api.models import (
    DocumentEncoding,
    DocumentLanguage,
    Project
    )
import esdoc_api.lib.utils.runtime as rt



class ESDOCSearchBase(object):
    """Base class for all search handlers.

    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = abc.ABCMeta


    def __init__(self, criteria_type, limit=2000):
        """Constructor.

        :param criteria_type: Type of search criteria handler.
        :type criteria_type: class

        :param limit: Limit upon number of records to return per search.
        :type limit: int

        """
        self.criteria_type = criteria_type
        self.limit = limit


    @abc.abstractproperty
    def criteria_type(self):
        """Gets type representing search criteria.

        """
        pass


    @abc.abstractmethod
    def set_query(self, ctx):
        """Sets query used to drive search process.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        pass


    @abc.abstractmethod
    def set_query_filter(self, ctx):
        """Applies query filters.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        pass


    def set_query_sort(self, ctx):
        """Applies query sorts.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        pass


    def set_query_offset(self, ctx):
        """Applies query offset.

        :param ctx: Contextual information driving search process.
        :type ctx: models.core.SearchContext

        """
        if ctx.q is not None:
            ctx.q = ctx.q.slice(0, self.limit)


    def do_search(self, criteria):
        """Invokes search.

        :param criteria: Search criteria.
        :type ctx: dict

        """
        # Initialise context.
        ctx = SearchContext(criteria)

        # Prepare query for execution.
        self.set_query(ctx)
        self.set_query_filter(ctx)
        self.set_query_sort(ctx)
        self.set_query_offset(ctx)

        # Execute.
        if ctx.q is not None:
            ctx.r = ctx.q.all()
            rt.log("SEARCH RETURNED :: {0} records".format(len(ctx.r)))

        # Format.
        if len(ctx.r) > 0 and hasattr(self, 'format_results'):
            ctx.r = self.format_results(ctx.r)

        return ctx.r


class ESDOCSearchCriteriaBase(object):
    """Encapsulates behaviours common to all search criteria.

    """
    # Abstract Base Class module - see http://docs.python.org/library/abc.html
    __metaclass__ = abc.ABCMeta


    def __init__(self):
        """Constructor.

        """
        for key in [k for k in self.keys]:
            setattr(self, key, None)


    def __str__(self):
        """Returns string representation.

        :returns: a string representation of the instance.
        :rtype: str

        """
        result = ''
        for key in [k for k in self.keys]:
            if len(result):
                result += ', '
            result += "{0} : {1}".format(key, getattr(self, key))
        return result


    @abc.abstractproperty
    def keys(self):
        """Gets list of criteria keys.

        :returns: a list of criteria keys.
        :rtype: string list

        """
        pass


    def hydrate(self, params):
        """Hydrates criteria state from dictionary of parameters.

        :param params: Search criteria parameters.
        :type params: dict

        """
        for key in [k for k in self.keys if k in params]:
            value = params[key]

            # set value.
            setattr(self, key, value)

            # format value.
            if hasattr(self, 'format_{0}'.format(key)):
                getattr(self, 'format_{0}'.format(key))()

            # set code.
            if hasattr(self, 'codes') and key in self.codes:
                try:
                    int(value)
                except ValueError:
                    value = self.codes[key](value.upper())
                    setattr(self, key, value.ID if value is not None else 0)


class BaseDocumentSearch(ESDOCSearchBase):
    """Base document search.

    """
    def __set_doc_metainfo(self):
        """Assigns document meta-information from incoming http request.

        """
        # Assign values.
        self.__set_doc_project()
        self.__set_doc_ontology()
        self.__set_doc_encoding()
        self.__set_doc_language()

        # Set flag indicating whether document metainfo is acceptable for document processing.
        self.is_doc_metainfo_valid = self.project is not None and \
                                     self.encoding is not None and \
                                     self.language is not None and \
                                     self.ontology is not None


    def __set_doc_project(self):
        """Assigns document project from incoming http request.

        """
        # Defensive programming.
        if not request.params.has_key('project'):
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Parameter project is unspecified')

        # Map to entity.
        self.project = c.get_project(request.params['project'])


    def __set_doc_encoding(self):
        """Assigns document encoding from incoming http request.

        """
        # Defensive programming.
        if not request.params.has_key('encoding'):
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Parameter encoding is unspecified')

        # Map to entity.
        self.encoding = c.get_encoding(request.params['encoding'])


    def __set_doc_language(self):
        """Assigns document language from incoming http request.

        """
        # Defensive programming.
        if not request.params.has_key('language'):
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Parameter language is unspecified')

        # Derive from url param (language).
        language_code = request.params['language']

        # Format (if appropriate).
        if isinstance(language_code, str):
            language_code = language_code.split('-')[0].lower()

        # Map to entity.
        self.language = c.get_language(language_code)


    def __set_doc_ontology(self):
        """Assigns document ontology from incoming http request.

        """
        # Defensive programming.
        if not request.params.has_key('ontologyName'):
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Parameter ontologyName is unspecified')
        if not request.params.has_key('ontologyVersion'):
            abort(HTTP_RESPONSE_BAD_REQUEST, 'Parameter ontologyVersion is unspecified')

        # Map to entity.
        self.ontology = c.get_ontology(request.params['ontologyName'],
                                       request.params['ontologyVersion'])



class BaseDocumentSearchCriteria(ESDOCSearchCriteriaBase):
    """Base document search criteria.

    """
    @property
    def keys(self):
        """Gets list of search criteria keys.

        :returns: A list of search criteria keys.
        :rtype: list

        """
        return ['project', 'encoding', 'language', 'ontology_name', 'ontology_version']


    @property
    def codes(self):
        """Gets list of search criteria codes.

        :returns: A list of search criteria codes.
        :rtype: list

        """
        return {
            'project' : Project.retrieve,
            'encoding' : DocumentEncoding.retrieve,
            'language' : DocumentLanguage.retrieve,
        }

    
    def format_encoding(self):
        self.encoding = self.encoding.lower()


    def format_language(self):
        self.language = self.language.upper()


    def format_ontology_name(self):
        self.ontology_name = self.ontology_name.lower()

    
    def format_ontology_version(self):
        self.ontology_version = self.ontology_version.upper()

    
    def format_project(self):
        self.project = self.project.upper()
