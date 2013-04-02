// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: Feedback :: Manages the process of displaying user feedback.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    var
        // Application related constants.
        _APP_NAME = 'Prodiguer',
        _APP_VERSION = '1.0b1',

        // Supported message types.
        _MESSAGE_TYPE_INFORMATION = 1,
        _MESSAGE_TYPE_CONFIRMATION = 2,
        _MESSAGE_TYPE_CONFIRMATION_WARNING = 6,
        _MESSAGE_TYPE_REDIRECT = 3,
        _MESSAGE_TYPE_VALIDATION = 4,
        _MESSAGE_TYPE_PROGRESS = 5,
        _MESSAGE_TYPE_FAILURE = 90,
        _MESSAGE_TYPE_ERROR = 99,

        // Standard messages.
        _STANDARD_MESSAGE_ERROR = 'A processing error has occurred ... please contact the system administrator.',

        // Wrapper around progess bar dialog.
        _progressBar = {
            // Queue of messages.
            messageQueue : [],

            // Jquery selectors in use by this widget.
            jqSelectors : {
                container : "#mfSiteProgress",
                message : "#mfSiteProgress .message"
            },

            // Resources used during various operations.
            resources : {
                dialogTitle : 'Processing request ... please wait',
                standardMessage : 'Processing request'
            },

            // Standard initialisation routine.
            initialise : function () {
                $jq(_progressBar.jqSelectors.container).
                    dialog({
                        bgiframe: true,
                        autoOpen: false,
                        height: 80,
                        width: 350,
                        position: ['center', 200],
                        modal: true });
                $jq(_progressBar.jqSelectors.container).dialog('option', 'title', _progressBar.resources.dialogTitle);
            },

            // Sets message.
            setMessage : function (message) {
                if (message === undefined) {
                    message = this.resources.standardMessage;
                }
                this.messageQueue.push(message);
                $jq(this.jqSelectors.message).text(this.messageQueue[0]);
            },

            // Displays dialog.
            display : function () {
                $jq(this.jqSelectors.container).dialog('open');
            },


            // Closes dialog.
            close : function () {
                $jq(this.jqSelectors.container).dialog('close');
                this.messageQueue = []
            }
        },

        // Wrapper around message box dialog.
        _messageBox = {
            // The jquery selectors in use by this widget.
            jqSelectors : {
                container : "#mfSiteFeedback",
                text : "#mfSiteFeedbackText",
                icon : "#mfSiteFeedbackIcon"
            },

            // Derives CSS suffix from type.
            getCssSuffix : function (type) {
                var
                    suffix = '';
                if (type === _MESSAGE_TYPE_INFORMATION) {
                    suffix += 'information';
                }
                else if (type === _MESSAGE_TYPE_CONFIRMATION) {
                    suffix += 'confirmation';
                }
                else if (type === _MESSAGE_TYPE_CONFIRMATION_WARNING) {
                    suffix += 'confirmation-warning';
                }
                else if (type === _MESSAGE_TYPE_REDIRECT) {
                    suffix += 'information';
                }
                else if (type === _MESSAGE_TYPE_VALIDATION) {
                    suffix += 'warning';
                }
                else if (type === _MESSAGE_TYPE_FAILURE) {
                    suffix += 'warning';
                }
                else if (type === _MESSAGE_TYPE_ERROR) {
                    suffix += 'error';
                }
                else {
                    suffix += 'information';
                }
                return suffix;
            },

            // Gets message text css according by message type.
            getTextCss : function (type) {
                var
                    result = "feedback-text feedback-text-";
                result += this.getCssSuffix(type);
                return result;
            },

            // Gets default message by message type.
            getDefaultText : function (type) {
                var result = "Unknown Message";
                if (type === _MESSAGE_TYPE_ERROR) {
                    result = _STANDARD_MESSAGE_ERROR;
                }
                return result;
            },

            // Resets dialog to initial state.
            reset : function () {
                $jq(this.jqSelectors.container).dialog("destroy");
                $jq(this.jqSelectors.container).removeAttr('title');
                $jq(this.jqSelectors.text).text("");
                $jq(this.jqSelectors.text).removeClass();
                $jq(this.jqSelectors.icon).text("");
                $jq(this.jqSelectors.icon).removeClass();
            },

            // Sets dialog caption.
            setCaption : function (caption, type) {
                var
                    derived = "";
                if (caption !== undefined) {
                    derived += caption;
                } else {
                    derived = _APP_NAME;
                    derived += " - ";
                    derived += "v";
                    derived += _APP_VERSION;
                }
                $jq(this.jqSelectors.container).attr('title', derived);
            },

            // Sets dialog icon.
            setIcon : function (type) {
                var
                    css = 'feedback-icon mf-icon-';
                css += this.getCssSuffix(type);
                css += '-32';
                $jq(this.jqSelectors.icon).attr('class', css);
            },

            // Sets dialog text.
            setText : function (text, type) {
                var
                    dialogText = text !== undefined ? text : this.getDefaultText(type),
                    dialogTextCss = this.getTextCss(type);
                $jq(this.jqSelectors.text)
                    .text(dialogText)
                    .attr('class', dialogTextCss);
            },

            // Returns an instance of the default dialog config.
            createDefaultConfig : function () {
                return {
                    width : 350,
                    position: ['center', 150],
                    modal: true
                }
            },

            // Displays the dialog with passed config.
            display : function (config) {
                $jq(this.jqSelectors.container).dialog(config);
            },

            // Displays standard one button mesage box.
            displayOneButton : function (continuation) {
                var
                    config = this.createDefaultConfig();
                config.buttons = {
                    'OK': function () {
                        $jq(this).dialog('close');
                        if ($jq.isFunction(continuation)) {
                            continuation();
                        }
                    }
                };
                this.display(config);
            },

            // Displays standard two button mesage box.
            displayTwoButton : function (continuation) {
                var
                    config = this.createDefaultConfig();
                config.buttons = {
                    'Yes': function () {
                        $jq(this).dialog('close');
                        if ($jq.isFunction(continuation)) {
                            continuation();
                        }
                    },
                    'No': function () {
                        $jq(this).dialog('close');
                    }
                };
                this.display(config);
            },

            // Closes associated dialog.
            close : function () {
                $jq(this.jqSelectors.container).dialog('close');
            },

            // Validates configuration.
            validateConfig : function (config) {
                // Validate required fields.
                if (config === undefined ||
                    config.type === undefined ||
                    config.text === undefined) {
                    throw {
                        name : 'MessageBoxError',
                        message : 'The message box configuration is invalid.'
                    };
                }
                // Validate message type.
                if (config.type !== _MESSAGE_TYPE_INFORMATION &&
                    config.type !== _MESSAGE_TYPE_CONFIRMATION &&
                    config.type !== _MESSAGE_TYPE_CONFIRMATION_WARNING &&
                    config.type !== _MESSAGE_TYPE_REDIRECT &&
                    config.type !== _MESSAGE_TYPE_VALIDATION &&
                    config.type !== _MESSAGE_TYPE_FAILURE &&
                    config.type !== _MESSAGE_TYPE_ERROR) {
                    throw {
                        name : 'MessageBoxError',
                        message : 'The message box type is unsupported.'
                    };
                }
            }
        },

        // Shows message box.
        _showMessage = function( config ) {
            // Ensure that progress bar is hidden.
            _progressBar.close();

            // Ensure that config is valid.
            _messageBox.validateConfig(config);

            // Intiialise dialog settings.
            _messageBox.reset();
            _messageBox.setCaption(config.caption, config.type);
            _messageBox.setText(config.text, config.type);
            _messageBox.setIcon(config.type);

            // Show approriate dialog.
            if (config.type === _MESSAGE_TYPE_INFORMATION) {
                _messageBox.displayOneButton(config.continuation);
            }
            else if (config.type === _MESSAGE_TYPE_CONFIRMATION) {
                _messageBox.displayTwoButton(config.continuation);
            }
            else if (config.type === _MESSAGE_TYPE_CONFIRMATION_WARNING) {
                _messageBox.displayTwoButton(config.continuation);
            }
            else if (config.type === _MESSAGE_TYPE_REDIRECT) {
                _messageBox.displayOneButton(config.continuation);
            }
            else if (config.type === _MESSAGE_TYPE_VALIDATION) {
                _messageBox.displayOneButton(config.continuation);
            }
            else if (config.type === _MESSAGE_TYPE_FAILURE) {
                _messageBox.displayOneButton(config.continuation);
            }
            else if (config.type === _MESSAGE_TYPE_ERROR) {
                _messageBox.displayOneButton(config.continuation);
            }
        },

        // Displays the progress bar.
        _showProgress = function (message) {
            _progressBar.setMessage(message);
            _progressBar.display();
        };

    // Register the widget and it's public members.
    $mf.registerWidget({
        id : 'feedback',
        initialise : function () { _progressBar.initialise(); },
        showMessage : _showMessage,
        showProgress : _showProgress,
        hideMessage : function () { _messageBox.close(); },
        hideProgress : function () { _progressBar.close(); },
        MESSAGE_TYPE_INFORMATION : _MESSAGE_TYPE_INFORMATION,
        MESSAGE_TYPE_CONFIRMATION : _MESSAGE_TYPE_CONFIRMATION,
        MESSAGE_TYPE_CONFIRMATION_WARNING : _MESSAGE_TYPE_CONFIRMATION_WARNING,
        MESSAGE_TYPE_REDIRECT : _MESSAGE_TYPE_REDIRECT,
        MESSAGE_TYPE_VALIDATION : _MESSAGE_TYPE_VALIDATION,
        MESSAGE_TYPE_PROGRESS : _MESSAGE_TYPE_PROGRESS,
        MESSAGE_TYPE_FAILURE : _MESSAGE_TYPE_FAILURE,
        MESSAGE_TYPE_ERROR : _MESSAGE_TYPE_ERROR
    });
}());