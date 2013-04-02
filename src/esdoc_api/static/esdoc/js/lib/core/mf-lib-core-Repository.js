// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: Repositry :: JS proxy to the repository service.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    var
        // The server side controller used to process data requests.
        _CONTROLLER = 'site/ajax',

        // Ajax helper used for making ajax callbacks.
        _ajax = $mf.ajaxHelper,

        // The resources used during various operations.
        _resources = {
            getEntityProgress : "Retrieving details"
        },

        // Returns an xhtml form for entering search criteria.
        _getSearchCriteriaForm = function (searchType, onSuccessHandler, onFailureHandler, progressMessage) {
            var
                // Ajax parameters.
                ajaxParams = { searchType : searchType },

                // Ajax call info.
                ajaxInfo = _ajax.createCallInfo(
                    _CONTROLLER,
                    'get_search_criteria_form',
                    ajaxParams,
                    _ajax.RESPONSE_TYPE_XHTML,
                    onSuccessHandler,
                    onFailureHandler,
                    progressMessage !== progressMessage
                );

            // Perform callback to retrieve criteria.
            _ajax.doGet(ajaxInfo);
        },

        // Returns search results based on the passed criteria.
        _getSearchResults = function (searchType, searchCriteriaJSON, onSuccessHandler, onFailureHandler, progressMessage, responseType) {
            var
                ajaxInfo,
                ajaxParams = searchCriteriaJSON;

            // Ajax parameters.
            ajaxParams.searchType = searchType;

            // Ajax call info.
            ajaxInfo = _ajax.createCallInfo(
                _CONTROLLER,
                'get_search_results',
                ajaxParams,
                responseType ? responseType : _ajax.RESPONSE_TYPE_XHTML,
                onSuccessHandler,
                onFailureHandler,
                progressMessage
            );

            // Perform ajax callback.
            _ajax.doGet(ajaxInfo);
        },

        // Returns an xhtml form for viewing/editing entity details.
        _getEntityDetailForm = function (entityType, onSuccessHandler, onFailureHandler, progressMessage) {
            var
                // Ajax parameters.
                ajaxParams = { entityType : entityType },

                // Ajax call info.
                ajaxInfo = _ajax.createCallInfo(
                    _CONTROLLER,
                    'get_entity_detail_form',
                    ajaxParams,
                    _ajax.RESPONSE_TYPE_XHTML,
                    onSuccessHandler,
                    onFailureHandler,
                    progressMessage
                );

            // Perform callback to retrieve criteria.
            _ajax.doGet(ajaxInfo);
        },

        // Retrieves an entity.
        _getEntity = function (entityType, entityID, onSuccessHandler, onFailureHandler, progressMessage) {
            var
                // Ajax parameters.
                ajaxParams = {
                    entityType : entityType,
                    entityID : entityID
                },

                // Ajax call info.
                ajaxInfo = _ajax.createCallInfo(
                    _CONTROLLER,
                    'get_entity',
                    ajaxParams,
                    _ajax.RESPONSE_TYPE_JSON,
                    onSuccessHandler,
                    onFailureHandler,
                    progressMessage !== undefined ? progressMessage : _resources.getEntityProgress
                );

            // Perform callback to retrieve criteria.
            _ajax.doGet(ajaxInfo);
        },

        // Retrieves an entity collection.
        _getEntityCollection = function (entityType, onSuccessHandler, onFailureHandler, progressMessage) {
            var
                // Ajax parameters.
                ajaxParams = {
                    entityType : entityType
                },

                // Ajax call info.
                ajaxInfo = _ajax.createCallInfo(
                    _CONTROLLER,
                    'get_entity_collection',
                    ajaxParams,
                    _ajax.RESPONSE_TYPE_JSON,
                    onSuccessHandler,
                    onFailureHandler,
                    progressMessage
                );

            // Perform callback to retrieve criteria.
            _ajax.doGet(ajaxInfo);
        },

        // Saves an entity.
        _saveEntity = function (entityType, entityID, entity, onSuccessHandler, onFailureHandler, progressMessage) {
            var
                // Ajax parameters.
                ajaxParams = {
                    entityType : entityType,
                    entityID : entityID,
                    entity : entity
                },

                // Ajax call info.
                ajaxInfo = _ajax.createCallInfo(
                    _CONTROLLER,
                    'save_entity',
                    ajaxParams,
                    _ajax.RESPONSE_TYPE_JSON,
                    onSuccessHandler,
                    onFailureHandler,
                    progressMessage
                );

            // Perform appropriate ajax call to process user input data.
            if (entityID === 0) {
                _ajax.doPost(ajaxInfo);
            } else {
                _ajax.doPut(ajaxInfo);
            }
        },

        // Deletes an entity.
        _deleteEntity = function (entityType, entityID, onSuccessHandler, onFailureHandler, progressMessage) {
            var
                // Ajax parameters.
                ajaxParams = {
                    entityType : entityType,
                    entityID : entityID
                },

                // Ajax call info.
                ajaxInfo = _ajax.createCallInfo(
                    _CONTROLLER,
                    'delete_entity',
                    ajaxParams,
                    _ajax.RESPONSE_TYPE_JSON,
                    onSuccessHandler,
                    onFailureHandler,
                    progressMessage
                );

            // Perform callback to retrieve criteria.
            _ajax.doGet(ajaxInfo);
        };

    // Register widget so that it is visible.
    $mf.registerWidget({
        id : 'repository',
        getSearchCriteriaForm : _getSearchCriteriaForm,
        getSearchResults : _getSearchResults,
        getEntityDetailForm : _getEntityDetailForm,
        getEntity : _getEntity,
        getEntityCollection : _getEntityCollection,
        deleteEntity : _deleteEntity,
        saveEntity : _saveEntity
    });
}());