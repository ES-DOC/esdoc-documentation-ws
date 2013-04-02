// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: searchEngine :: Encapsulates search related operations.
// --------------------------------------------------------
(function () {
    // Private members.
    var
        // The collection of search managers.
        _managers = [],

        // Standard initialisation routine.
        _initialise = function () {
            var
                i,
                controller;
            for (i = 0; i < _managers.length; i++) {
                controller = _managers[i];
                if (controller.info.autoBegin === true) {
                    controller.actions.begin();
                }
            }
        },

        // Factory method to create a criteria fields manager.
        _createCriteriaFieldsManager = function () {
            var
                // Collection of managed criteria.
                _fieldCollection = [],

                // Gets a field from collection.
                _getField = function (fieldSelector) {
                    var
                        i,
                        item,
                        result;
                    for (i = 0; i < _fieldCollection.length; i++) {
                        item = _fieldCollection[i];
                        if (item.jqSelector === fieldSelector) {
                            result = item;
                            break
                        }
                    }
                    return result;
                };

            return {
                // Initialises fields from an html form.
                initialise : function (formSelector) {
                    var
                        appendField = function (fieldSelector) {
                            var field = {
                                jqSelector : fieldSelector,
                                defaultVal : $jq(fieldSelector).val(),
                                getCurrentVal : function () {
                                    return $jq(fieldSelector).val();
                                },
                                triggerChangeEvent : function () {
                                    $jq(fieldSelector).trigger('change');
                                }
                            };
                            _fieldCollection.push(field);
                        };
                    $jq(formSelector + ' input').each(function () {
                        appendField(formSelector + ' #' + $jq(this).attr('id'));
                    });
                    $jq(formSelector + ' select').each(function () {
                        appendField(formSelector + ' #' + $jq(this).attr('id'));
                    });
                },

                // Applies criteria by triggering change events.
                apply : function () {
                    var
                        i;
                    for (i = 0; i < _fieldCollection.length; i++) {
                        _fieldCollection[i].triggerChangeEvent();
                    }
                },

                // Returns current state of all fields.
                getState : function () {
                    var
                        i,
                        result = '';
                    for (i = 0; i < _fieldCollection.length; i++) {
                        result += _fieldCollection[i].getCurrentVal();
                    }
                    return result;
                },

                // Applies default criteria.
                reset : function () {
                    $mf.uiUtils.setValueOfInputCollection(_fieldCollection)
                },

                // Gets default value for a criteria item.
                getDefaultVal : function (fieldSelector) {
                    var
                        item = _getField(fieldSelector),
                        result;
                    if (item !== undefined) {
                        result = item.defaultVal;
                    }
                    return result;
                },

                // Sets default value for a criteria item.
                setDefaultVal : function (fieldSelector, defaultVal) {
                    var
                        item = _getField(fieldSelector);
                    if (item !== undefined) {
                        item.defaultVal = defaultVal;
                    }
                }
            }
        },

        // Factory method to create a search controller.
        _create = function (spec) {
            // Validate spec.
            if (spec === undefined ||
                spec.searchType === undefined) {
                throw {
                    name : 'SearchControllerFactoryError',
                    message : 'The controller specification is invalid.'
                };
            }

            // Private members.
            var
                // Search meta-information.
                _info = {
                    // Type of search being managed.
                    searchType : spec.searchType,

                    // Initialisation flag.
                    isInitialised : false,

                    // Flag indicating whether search process will be automatically started.
                    autoBegin : spec.autoBegin !== undefined ? spec.autoBegin : false,

                    // Config used to render assoiated data table.
                    dtConfig : spec.dataTableConfig,

                    // Flag indicating whether data table will be auto-rendered.
                    renderDataTable : spec.renderDataTable !== undefined ? spec.renderDataTable : true,

                    // Flag indicating whether initial search results will be cached or not.
                    cacheInitialResults : spec.cacheInitialResults !== undefined ? spec.cacheInitialResults : true
                },

                // User interface specific information/behaviour.
                _ui = {
                    // The jquery selectors in use by this widget.
                    jqSelectors : {
                        container : '#mfSearch_' + spec.searchType,
                        buttonbar : {
                            container : '#mfSearch_' + spec.searchType + ' .mf-search-criteria-toolbar',
                            searchButton : '#mfSearch_' + spec.searchType + ' .mf-search-criteria-toolbar  .mf-search-button',
                            resetButton : '#mfSearch_' + spec.searchType + ' .mf-search-criteria-toolbar  .mf-search-reset-button'
                        },
                        criteria : {
                            container : '#mfSearch_' + spec.searchType + ' .mf-search-criteria',
                            form : '#mfSearch_' + spec.searchType + ' .mf-search-criteria-form form',
                            formContainer : '#mfSearch_' + spec.searchType + ' .mf-search-criteria-form'
                        },
                        results : {
                            container : '#mfSearch_' + spec.searchType + ' .mf-search-results',
                            table : '#mfSearch_' + spec.searchType + ' .mf-search-results table'
                        }
                    },

                    // The resources used during various operations.
                    resources : {
                        initialisationProgress : 'Initializing Search Engine',
                        executionProgress : 'Searching Repository',
                        resetProgress : 'Resetting Search Engine',
                        errorCaption : 'Server Side Error',
                        errorMessage : 'An error occurred whilst processing the search request.  Please contact system administrator if this continues.'
                    },

                    // Search buttonbar.
                    buttonbar : {
                        // Initialises the buttonbar buttons.
                        initialise : function () {
                            var
                                onSearch = function () {
                                    if (_ui.criteria.requiresSearch() === true) {
                                        _actions.execute();
                                    }
                                },
                                onSearchReset = function () {
                                    if (_ui.criteria.requiresSearchReset() === true) {
                                        _actions.reset();
                                    }
                                };
                            $jq(_ui.jqSelectors.buttonbar.searchButton).button({
                                icons : {
                                    primary : 'ui-icon-search'
                                },
                                text : spec.displaySearchButtonText === false ? false : true
                            }).bind('click', onSearch);
                            $jq(_ui.jqSelectors.buttonbar.resetButton).button({
                                icons : {
                                    primary : 'ui-icon-refresh'
                                },
                                text : spec.displayCancelButtonText === true ? true : false
                            }).bind('click', onSearchReset);
                        }
                    },

                    // Search criteria.
                    criteria : (function () {
                        var
                            // Fields manager for tracking, setting state of criteria fields.
                            _fields = _createCriteriaFieldsManager(),

                            // State of criteria both initially & after previous search.
                            _state = {
                                initial : undefined,
                                previous : undefined
                            };

                        return {
                            // Returns a JSON representation.
                            toJSON : function () {
                                return $mf.uiUtils.getFormAsJSON(_ui.jqSelectors.criteria.form);
                            },

                            // Sets associated xhtml form.
                            setXhtml : function (xhtml) {
                                $jq(_ui.jqSelectors.criteria.formContainer).html(xhtml);
                                _fields.initialise(_ui.jqSelectors.criteria.form);
                            },

                            // Resets crtieria form values.
                            reset : function () {
                                _fields.reset();
                                this.setPreviousState();
                            },

                            // Standard initialisation routine.
                            setInitialState : function () {
                                _state.initial = _fields.getState();
                            },

                            // Updates current state after a search.
                            setPreviousState : function () {
                                _state.previous = _fields.getState();
                            },

                            // Determines whether a search is required.
                            requiresSearch : function () {
                                var
                                    result = false,
                                    stateCurrent = _fields.getState();
                                if (stateCurrent !== _state.previous) {
                                    result = true;
                                }
                                return result;
                            },

                            // Determines whether a search reset is required.
                            requiresSearchReset : function () {
                                var
                                    result = false,
                                    stateCurrent = _fields.getState();
                                if (stateCurrent !== _state.initial) {
                                    result = true;
                                }
                                return result;
                            }
                        }
                    }()),

                    // Search results.
                    results : (function () {
                        var
                            // Flag indicating whether results have already been loaded.
                            _isLoaded = false;

                        return {
                            // Sets associated xhtml form.
                            setXhtml : function (data) {
                                // Use initial results (if necessary).
                                if (data === undefined) {
                                    data = $jq(_ui.jqSelectors.container).data('initialState');
                                }

                                // Set initial state (if necessary).
                                if ($jq(_ui.jqSelectors.container).data('initialState') === undefined) {
                                    $jq(_ui.jqSelectors.container).data('initialState', data);
                                }

                                // Update criteria state.
                                _ui.criteria.setPreviousState();

                                // Assign html.
                                $jq(_ui.jqSelectors.results.container).html(data);

                                // Render data table.
                                $jq(_ui.jqSelectors.container).show();
                                if (_info.onResultsRendering === true) {
                                    // note - data table container must be visible  in order to render correctly.
                                    _events.onResultsRendering.publish();
                                    $mf.grid.render(_ui.jqSelectors.results.table, _info.dtConfig);
                                    _events.onResultsRendered.publish();
                                }

                                // Set flag.
                                _isLoaded = true;
                            },

                            // Gets initial search results from internal cache.
                            getCachedState : function () {
                                return $jq(_ui.jqSelectors.container).data('initialState');
                            },

                            // Gets flag indicating whether initial search results have been cached or not.
                            hasCachedState : function () {
                                return $jq(_ui.jqSelectors.container).data('initialState') !== undefined;
                            },

                            // Flag indicating whether results have already been loaded.
                            isLoaded : _isLoaded
                        }
                    }())
                },

                // Event publishers.
                _events = {
                    // Event raised when the search criteria form has been loaded.
                    onCriteriaInitialising : $mf.createEventPublisher(),

                    // Event raised when the search criteria form is ready for use.
                    onCriteriaInitialised : $mf.createEventPublisher(),

                    // Event raised when a search reset is to be executed.
                    onResetting : $mf.createEventPublisher(),

                    // Event raised when a search reset is to be executed.
                    onReset : $mf.createEventPublisher(),

                    // Event raised when a search is to be executed.
                    onExecuting : $mf.createEventPublisher(),

                    // Event raised when a search has been executed.
                    onExecution : $mf.createEventPublisher(),

                    // Event raised when a search has been executed and the result assigned.
                    onResultsAssigned : $mf.createEventPublisher(),

                    // Event raised when a search has been executed and the result about to be rendered.
                    onResultsRendering : $mf.createEventPublisher(),

                    // Event raised when a search has been executed and the results rendered.
                    onResultsRendered : $mf.createEventPublisher(),

                    // Event raised when an error has occurred.
                    onError : $mf.createEventPublisher(),

                    // Standard initialisation routine.
                    initialise : function () {
                        this.onError.bind( function (jqXHR, textStatus, errorThrown) {
                            var
                                messageInfo = {
                                    type : $mf.feedback.MESSAGE_TYPE_ERROR,
                                    caption : _ui.resources.errorCaption,
                                    text : _ui.resources.errorMessage
                                };
                            $mf.feedback.showMessage(messageInfo);
                        });
                        this.onCriteriaInitialising.bind( function () {
                            $mf.uiUtils.setFormTabIndexes(_ui.jqSelectors.criteria.form);
                        });
                        this.onCriteriaInitialised.bind( function () {
                            _ui.criteria.setInitialState();
                            _ui.buttonbar.initialise();
                        });
                        this.onResetting.bind( function () {
                            _ui.criteria.reset();
                        });
                        this.onReset.bind( function () {
                            _actions.execute();
                        });
                        this.onExecuting.bind( function () {
                            $mf.feedback.showProgress(_ui.resources.executionProgress);
                        });
                        this.onExecution.bind( function (data) {
                            $mf.uiUtils.destroyClipboardHelpers();
                            _ui.results.setXhtml(data);
                            _events.onResultsAssigned.publish();
                            $mf.feedback.hideProgress();
                        });
                    }
                },

                // Search actions.
                _actions = {
                    // Begin search process.
                    begin : function () {
                        var
                            // Callback to handle get criteria success event.
                            onCriteriaFormLoad = function (data) {
                                // Render UI.
                                _ui.criteria.setXhtml(data);

                                // Publish events.
                                _events.onCriteriaInitialising.publish();
                                _events.onCriteriaInitialised.publish();

                                // Avoid re-initialisation.
                                _info.isInitialised = true;

                                // Auto-execute search.
                                _actions.execute(true);
                            };

                        // Display or initialise (as appropriate).
                        if (_info.isInitialised === true) {
                            $jq(_ui.jqSelectors.container).show();
                        } else {
                            $mf.feedback.showProgress(_ui.resources.initialisationProgress);
                            setTimeout(function () {
                                _events.initialise();
                                $mf.repository.getSearchCriteriaForm(_info.searchType, onCriteriaFormLoad, _events.onError.publish)
                            }, 50);
                        }
                    },

                    // Execute search.
                    execute : function () {
                        _events.onExecuting.publish();
                        $mf.repository.getSearchResults(_info.searchType,
                                                          _ui.criteria.toJSON(),
                                                          _events.onExecution.publish,
                                                          _events.onError.publish);
                    },

                    // Reset the search process.
                    reset : function () {
                        $mf.feedback.showProgress(_ui.resources.resetProgress);
                        setTimeout(function () {
                            _events.onResetting.publish();
                            _events.onReset.publish();
                        }, 50);
                    },

                    // Ends the search process.
                    end : function () {
                        $jq(_ui.jqSelectors.container).hide();
                    }
                },

                // Instantiate, store & return.
                newManager = {
                    info : _info,
                    events : _events,
                    actions : _actions
                };
            _managers.push(newManager);
            return newManager;
        };

    // Register widget so that it is visible.
    $mf.registerWidget({
        id : 'searchEngine',
        initialise : _initialise,
        createCriteriaFieldsManager : _createCriteriaFieldsManager,
        create : _create
    });
}());