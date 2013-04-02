// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: PageToolbar :: Manages page toolbar event handling.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    var
        // Current active partition.
        _currentPartition = undefined,

        // Current active button.
        _currentButton = undefined,

        // Set of button options.
        _buttonOptions = [],

        // Gets button options.
        _getOptions = function (buttonID) {
            var
                i,
                options;
            for (i = 0; i < _buttonOptions.length; i++) {
                options = _buttonOptions[i];
                if (options.buttonID === buttonID) {
                    return options;
                }
            }
            return undefined;
        },

        // The jquery selectors in use by this widget.
        _jqs = {
            pageHeaderTitle : ".mf-page .inner .header .title",
            pagePartitionSet : ".mf-site-header .inner .menu .secondary .partition-set",
            pagePartition : ".mf-site-header .inner .menu .secondary .partition-set .partition",
            pageActionSet : ".mf-site-header .inner .menu .secondary .action-set",
            pageAction : ".mf-site-header .inner .menu .secondary .action-set .action"
        },

        // Deactivate previous button.
        _deactivate = function () {
            if (_currentButton !== undefined) {
                _events.onItemClose.publish(_currentButton);
            }
        },

        // Activate clicked button.
        _activate = function (button) {
            if (button !== undefined) {
                _currentButton = button;
                _events.onItemOpen.publish(button);
            }
        },

        // Resets button so that it can be reinvoked.
        _resetButton = function () {
            if (_currentButton !== undefined) {
                _currentButton = undefined;
            }
        },

        // Button click event handler.
        _onButtonClick = function () {
            var options;
            if (_currentButton === undefined ||
                _currentButton.id !== this.id) {
                options = _getOptions(this.id);
                if (options !== undefined && options.isDialog === true) {
                    _events.onItemOpen.publish(this);
                } else {
                    _deactivate();
                    _activate(this);
                }
            }
        },

        // Page partition click event handler.
        _onPagePartitionClick = function () {
            if (_currentPartition === undefined ||
                _currentPartition.id !== this.id) {
                if (_currentPartition !== undefined) {
                    _events.onPartitionClose.publish(_currentPartition);
                }
                _currentPartition = this;
                _events.onPartitionOpen.publish(_currentPartition);
            }
        },

        // Page function click event handler.
        _onPageFunctionClick = function () {
            _events.onFunctionInvoke.publish(this);
        },

        // Standard initialisation routine.
        _initialise = function () {
            var
                i;
            if ($jq(_jqs.pagePartition).length > 0) {
                $jq(_jqs.pagePartition)
                    .bind('click', _onPagePartitionClick);
            }
            if ($jq(_jqs.pageAction).length > 0) {
                $jq(_jqs.pageAction)
                    .bind('click', _onPageFunctionClick);
            }
        },

        // Assigns page header text.
        _setPageHeaderText = function (text) {
            $jq(_jqs.pageHeaderTitle).text(text);
        },

        // Event publishers.
        _events = {
            // Event raised when a partition is being closed.
            onPartitionClose : $mf.createEventPublisher(),

            // Event raised when a partition is being opened.
            onPartitionOpen : $mf.createEventPublisher(),

            // Event raised when a function is about to be invoked.
            onFunctionInvoke : $mf.createEventPublisher(),

            // Event raised when a function has been invoked.
            onFunctionInvoked : $mf.createEventPublisher(),

            // Event raised when an item is being closed.
            onItemClose : $mf.createEventPublisher(),

            // Event raised when an item is being opened.
            onItemOpen : $mf.createEventPublisher()
        },

        // Assigns button specific options.
        _registerButtonOptions = function (options) {
            var
                validateOptions = function() {
                    // Validate required fields.
                    if (options === undefined ||
                        options.buttonID === undefined ||
                        options.isDialog === undefined) {
                        throw {
                            name : 'ToolbarError',
                            message : 'The toolbar options are invalid.'
                        };
                    }
                };
             // Ensure options are valid.
             validateOptions();
             // Add to collection.
             _buttonOptions.push(options);
        },

        // Activates initiali partition.
        _activateInitialPartition = function () {
            if ($jq(_jqs.pagePartition).length > 0) {
                $jq(_jqs.pagePartition)
                    .first()
                    .trigger('click');
            }
        };

    // Event handler for page toolbar partition open event.
    _events.onPartitionOpen.bind(function (item) {
        $jq("#" + item.id).addClass('current');
        $jq("#" + item.id + '-content').toggle();
    });

    // Event handler for page toolbar partition close event.
    _events.onPartitionClose.bind(function (item) {
        $jq("#" + item.id).removeClass('current');
        $jq("#" + item.id + '-content').toggle();
    });

    // Register widget so that it is visible.
    $mf.registerWidget({
        id : 'toolbar',
        initialise : _initialise,
        resetButton : _resetButton,
        events : _events,
        setPageHeaderText : _setPageHeaderText,
        registerButtonOptions : _registerButtonOptions,
        activateInitialPartition : _activateInitialPartition
    });

}());