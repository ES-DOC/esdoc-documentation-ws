// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: ajaxHelper :: Encapsulates all ajax callback helper functions.
// --------------------------------------------------------
(function () {
    var
        // JQuery selectors used in this widget.
        _jqs = {
            key : '#mfPageDataKey'
        },

        // Resources used during various operations.
        _resources = {
            progressMessage : 'Loading page data'
        },

        // Loads data into memory via ajax call.
        _load = function (dataKey, callback) {
            var
                ajaxCallbackHandler = function (json) {
                    _events.onDataLoaded.publish({
                        key : dataKey,
                        json : json
                    })
                    if ($jq.isFunction(callback) === true) {
                        callback(json);
                    }
                },
                ajaxInfo = $mf.ajaxHelper.createCallInfo(
                    'site/ajax',
                    'get_data',
                    { key : dataKey },
                    $mf.ajaxHelper.RESPONSE_TYPE_JSON,
                    ajaxCallbackHandler,
                    null,
                    _resources.progressMessage
                );
            // Publish loading event.
            _events.onDataLoading.publish();
            // Retrieve data from server.
            $mf.ajaxHelper.doGet(ajaxInfo);
        },

        // Set of actions exposed by this widget.
        _actions = {
            load : _load
        },

        // Set of events exposed by this widget.
        _events = {
            // Event raised when page data is about to load.
            onDataLoading : $mf.createEventPublisher(),

            // Event raised when page data has been loaded.
            onDataLoaded : $mf.createEventPublisher()
        };

    // Register the widget and it's public members.
    $mf.registerWidget({
        id : 'dataLoader',
        actions : _actions,
        events : _events
    });
}());