// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: ajaxHelper :: Encapsulates all ajax callback helper functions.
// --------------------------------------------------------
(function () {
    var
        // HTTP related constants.
        _BASE_URL = '/{0}/{1}',
        _RESPONSE_TYPE_JSON = 'json',
        _RESPONSE_TYPE_XHTML = 'xhtml',
        _RESPONSE_TYPE_XML = 'xml',

        // Standard callback error handler.
        _standardErrorHandler = function (e, xhr, settings, exception) {
            // TODO Formalise error actions.
            alert('An AJAX callback error - please inform site administrator.');
        },

        // Standard callback success handler.
        _standardSuccessHandler = function () {
            return;
        },

        // Returns the url mapping to a controller action.
        _getUrl = function (controller, action) {
            return _BASE_URL.replace('{0}', controller).replace('{1}', action);
        },

        // Factory method to create ajax callback information.
        _createCallInfo = function (controller, action, data, responseType, successHandler, errorHandler, progressInfo) {
            var
                result = {};
            result.requestUrl = _getUrl(controller, action);
            result.requestData = data !== undefined ? data : {};
            result.responseType = responseType !== undefined ? responseType : _RESPONSE_TYPE_XHTML;
            result.responseHandler = successHandler !== undefined ? successHandler : _standardSuccessHandler;
            result.responseErrorHandler = errorHandler !== undefined ? errorHandler : _standardErrorHandler;
            result.progressInfo = progressInfo;
            return result;
        },

        // Executes an ajax call.
        _doAjaxCall = function (callInfo) {
            // Set progress bar message.
            if (callInfo.progressInfo !== undefined) {
                $mf.feedback.showProgress(callInfo.progressInfo);
            }

            // Use jquery to perform callback.
            $jq.ajax({
                type: callInfo.requestType,
                url: callInfo.requestUrl,
                data: callInfo.requestData,
                dataType: callInfo.responseType,
                global: false,
                success: callInfo.responseHandler,
                error: callInfo.responseErrorHandler
            });
        },

        // Executes an ajax get.
        _doGet = function (callInfo) {
            callInfo.requestType = 'GET';
            _doAjaxCall(callInfo);
        },

        // Executes an ajax delete.
        _doDelete = function (callInfo) {
            callInfo.requestType = 'DELETE';
            _doAjaxCall(callInfo);
        },

        // Executes an ajax post.
        _doPost = function (callInfo) {
            callInfo.requestType = 'POST';
            _doAjaxCall(callInfo);
        },

        // Executes an ajax put.
        _doPut = function (callInfo) {
            callInfo.requestType = 'PUT';
            _doAjaxCall(callInfo);
        };

    // Register the widget and it's public members.
    $mf.registerWidget({
        id : 'ajaxHelper',
        createCallInfo : _createCallInfo,
        doGet : _doGet,
        doDelete : _doDelete,
        doPost : _doPost,
        doPut : _doPut,
        RESPONSE_TYPE_JSON : _RESPONSE_TYPE_JSON,
        RESPONSE_TYPE_XHTML : _RESPONSE_TYPE_XHTML,
        RESPONSE_TYPE_XML : _RESPONSE_TYPE_XML
    });
}());