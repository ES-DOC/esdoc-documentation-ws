// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: UIHelper :: Provides UI helper functions.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    var
        // Refills a combo-box.
        _doComboBoxRefill = function (config) {
            var
                target = config.target,
                i,
                item,
                html = '';

            // Set default null settings.
            if (config.nullSettings === undefined) {
                config.nullSettings = {display : true, value : "0", text : ""};
            }
            if (config.nullSettings.display === undefined) {
                config.nullSettings.display = true;
            }
            if (config.nullSettings.value === undefined) {
                config.nullSettings.value = 0;
            }
            if (config.nullSettings.text === undefined) {
                config.nullSettings.text = "";
            }

            // Set default callbacks.
            if (config.target.useItem === undefined) {
                config.target.useItem = function (item) {
                    return true;
                }
            }
            if (config.target.getItemValueCallback === undefined) {
                config.target.getItemValueCallback = function (item) {
                    return item.ID;
                }
            }
            if (config.target.getItemTextCallback === undefined) {
                config.target.getItemTextCallback = function (item) {
                    return item.Name;
                }
            }
            if (config.target.getItemIsDefaultCallback === undefined) {
                config.target.getItemIsDefaultCallback = function (item) {
                    return false;
                }
            }

            // Null value.
            if (config.nullSettings.display === true) {
                html += '<option value="';
                html += config.nullSettings.value;
                html += '">';
                html += config.nullSettings.text;
                html += '</option>';
            }

            // Collection values.
            for (i = 0; i < target.data.length; i++) {
                item = target.data[i];
                if (target.useItem(item)) {
                    html += '<option ';
                    if (target.getItemIsDefaultCallback(item) === true) {
                        html += 'selected="true" ';
                    }
                    html += 'value="';
                    html += target.getItemValueCallback(item);
                    html += '">';
                    html += target.getItemTextCallback(item);
                    html += '</option>';
                }
            }

            // Refill selector.
            $jq("#" + config.target.ID).html(html);
        },

        // Handles the cascade from one combo box to another.
        _doComboBoxCascade = function (cascadeConfig) {
            var
                config = cascadeConfig,
                sourceValue = parseInt($jq("#" + config.source.ID).val()),
                useItem,
                getItemValue,
                getItemText,
                getItemFilter = config.target.getItemFilter,
                nullSettings = config.nullSettings,
                data = config.target.data,
                defaultData = config.target.defaultData,
                item,
                itemValue,
                itemText,
                target,
                targetPrevious,
                html = '',
                triggerChangeEvent = true,
                i,
                filteredData = [];

            // Set defaults where appropriate.
            useItem = config.target.useItem;
            if (useItem === undefined) {
                useItem = function (item) {return true;};
            }
            getItemValue = config.target.getItemValue;
            if (getItemValue === undefined) {
                getItemValue = function (item) {return item.ID;};
            }
            getItemText = config.target.getItemText;
            if (getItemText === undefined) {
                getItemText = function (item) {return item.Name;};
            }
            if (nullSettings === undefined) {
                nullSettings = {display : true, value : "0", text : ""};
            }
            if (nullSettings.display === undefined) {
                nullSettings.display = true;
            }
            if (nullSettings.value === undefined) {
                nullSettings.value = 0;
            }
            if (nullSettings.text === undefined) {
                nullSettings.text = "";
            }

            // Filter output frequencies as appropriate.
            switch(sourceValue)
            {
                case 0:
                    filteredData = defaultData !== undefined ? defaultData : data;
                    break;
                default:
                    for (i = 0; i < data.length; i++) {
                        target = data[i];
                        if (getItemFilter(target) === sourceValue) {
                            filteredData.push(target);
                        }
                    }
                    break;
            }

            // Get previous frequency.
            targetPrevious = parseInt($jq("#" + config.target.ID).val());

            // Rebuild combo box:
            // ... null value;
            if (nullSettings.display === true) {
                html += '<option value="';
                html += nullSettings.value;
                html += '">';
                html += nullSettings.text;
                html += '</option>';
            }
            // ... data items;
            for (i = 0; i < filteredData.length; i++) {
                item = filteredData[i];
                if (useItem(item)) {
                    itemValue = getItemValue(item);
                    itemText = getItemText(item);
                    html += '<option value="';
                    html += itemValue;
                    if (targetPrevious !== undefined &&
                        targetPrevious > 0 &&
                        targetPrevious === parseInt(itemValue)) {
                        triggerChangeEvent = false;
                        html += '" selected="true';
                    }
                    html += '">';
                    html += itemText;
                    html += '</option>';
                }
            }
            $jq("#" + config.target.ID).html(html);

            // Trigger change event.
            if (triggerChangeEvent) {
                $jq("#" + config.target.ID).trigger('change');
            }

            // Call continuation function if provided.
            if ($jq.isFunction(cascadeConfig.continuation)) {
                cascadeConfig.continuation();
            }
        },

        // Sets locked status of a form.
        _setFormLockedState = function (formSelector, lockedState) {
            if (lockedState === true) {
                $jq(formSelector + ' input').attr("disabled", "disabled");
                $jq(formSelector + ' select').attr("disabled", "disabled");
            } else {
                $jq(formSelector + ' input').removeAttr("disabled");
                $jq(formSelector + ' select').removeAttr("disabled");
            }
        },

        // Sets the form change handler.
        _setFormChangedHandler = function (formSelector, onFormChangeCallback) {
            $jq(formSelector  + ' input').change(onFormChangeCallback)
            $jq(formSelector  + ' select').change(onFormChangeCallback)
        },

        // Counter over number of times the tab indexer is called.
        formTabIndexesCounter = 1,

        // Sets tab indexes across form elements.
        _setFormTabIndexes = function (formSelector) {
            var
                tabindex = formTabIndexesCounter * 100,
                formInputControlSelector = formSelector + " :input";
            formTabIndexesCounter++;
            $jq(formInputControlSelector).each(function() {
                if (this.type != "hidden") {
                    var $input = $jq(this);
                    $input.attr("tabindex", tabindex);
                    tabindex++;
                }
            });
        },

        // Returns form input fields as a json (dictionary).
        _getFormAsJSON = function (formSelector) {
            var
                inputs = $jq(formSelector + " :input"),
                result = {},
                obj = $jq.map(inputs, function(n, i)
                {
                    result[n.name] = $jq(n).val();
                });
            return result;
        },

        // Returns form input fields as a string.
        _getFormAsString = function (formSelector) {
            var
                inputs = $jq(formSelector + " :input"),
                result = "",
                obj = $jq.map(inputs, function(n, i)
                {
                    result += $jq(n).val();
                });
            return result;
        },

        // Sets value of an input control.
        _setValueOfInput = function (inputSelector, inputValue) {
            var
                current;
            current = $jq(inputSelector).val();
            if (current !== inputValue) {
                $jq(inputSelector).val(inputValue).trigger('change');
            }
        },

        // Sets value of an= collection of input controls.
        _setValueOfInputCollection = function (inputCollection) {
            var
                i,
                input;
            for (i = 0; i < inputCollection.length; i++) {
                input = inputCollection[i];
                _setValueOfInput(input.jqSelector, input.defaultVal);
            }
        },

        // Opens the target url.
        _openURL = function(url, inTab) {
            if (inTab === true) {
                window.open(url);
            } else {
                window.location = url;
            }
        },

        // Performs a post to the target url.
        _postToURL = function (url, params, newWindow) {
            var
                form = $jq('<form>');
            form.attr('action', url);
            form.attr('method', 'POST');
            if (newWindow === true) {
                form.attr('target', '_blank');
            }

            var addParam = function(paramName, paramValue){
                var input = $jq('<input type="hidden">');
                input.attr({'id':     paramName,
                             'name':   paramName,
                             'value':  paramValue});
                form.append(input);
            };

            // Params is an Array.
            if(params instanceof Array){
                for(var i=0; i<params.length; i++){
                    addParam(i, params[i]);
                }
            }

            // Params is an Associative array or Object.
            if(params instanceof Object){
                for(var key in params){
                    addParam(key, params[key]);
                }
            }

            // Submit the form, then remove it from the page
            form.appendTo(document.body);
            form.submit();
            form.remove();
        },

        // Gets a formatted date.
        _getDate = function ( selector, format ) {
            var
                result = null,
                date;
            if (selector) {
                if (format === undefined) {
                    format = 'yy-mm-dd';
                }
                date = $jq(selector).val()
                if (date) {
                    date = $jq.datepicker.parseDate(format, date);
                    result = $jq.datepicker.formatDate(format, date);
                }
            }
            return result;
        },

        // Sets a formatted date.
        _setDate = function ( selector, date, format ) {
            var
                value = '';
            if (selector) {
                if (date) {
                    if (format === undefined) {
                        format = 'yy-mm-dd';
                    }
                    value = $jq.datepicker.formatDate(format, $jq.datepicker.parseDate(format, date));
                }
                $jq(selector).val(value);
            }
        },

        // Extracts & returns the file extension from the passed filename.
        _getFileExtension = function (filename) {
            var
                extensionRegExp = /.+\.([^.]+)$/,
                result = "";
            if (filename !== "") {
                var matches = extensionRegExp.exec(filename);
                if (matches.length > 0) {
                    result = matches[1];
                }
            }
            return result.toString().toUpperCase();
        },

        // Validates a file for upload.
        _validateFileForUpload = function (fileUploader, fileType, fileSizeInMB, invalidFileTypeMessage) {
            var
                resources = {
                    emptyFileTitle : "Empty File",
                    emptyFileMessage : "Please specify a filename.",
                    invalidFileTypeTitle : "Invalid File Type",
                    invalidFileTypeMessage : invalidFileTypeMessage !== undefined ? invalidFileTypeMessage : "File type is unsupported - please choose another file."
                },
                messageInfo = {
                    type : $mf.feedback.MESSAGE_TYPE_VALIDATION
                },
                file = $jq(fileUploader).val(),
                isValid = true;

            // False if empty file.
            if (file === null || file === undefined || file == ""){
                messageInfo.caption = resources.emptyFileTitle;
                messageInfo.text = resources.emptyFileMessage;
                isValid = false;
            }

            // False if not an xml file.
            if (isValid) {
                if (fileType !== _getFileExtension(file)) {
                    messageInfo.caption = resources.invalidFileTypeTitle;
                    messageInfo.text = resources.invalidFileTypeMessage;
                    isValid = false;
                }
            }

            // False if file larger than allowed limit.
            // TODO

            // Display validation message if necessary.
            if (isValid === false) {
                $mf.feedback.showMessage(messageInfo);
                $jq(fileUploader).focus();
            }

            // Return validation state.
            return isValid;
        },

        // Returns query param value.
        _getURLParam = function(name, defaultValue) {
            var
                results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
            if (!results) {
                return defaultValue;
            }
            return results[1] || defaultValue;
        },

        // Creates clipboard helper object.
        _createClipboardHelper = function(config) {
            var
                clip,
                clips = [], f;
            // Destroy.
            _destroyClipboardHelpers();

            // Create.
            if (config.jqSelector === undefined) {
                config.jqSelector = '.ui-icon-clipboard';
            }
            $(config.jqSelector).each(function () {
                var clip = new ZeroClipboard.Client();
                clip.glue( this );
                clip.setText( $(this).text() );
                if ($jq.isFunction(config.onCopyCallback)) {
                    clip.addEventListener( 'complete', config.onCopyCallback );
                }
                clips.push(clip);
            });

            // Cache;
            $jq("#mfWidgets").data('zeroClipboard', clips);
            f = $jq("#mfWidgets").data('zeroClipboard');
        },

        // Destroys clipboard helper object.
        _destroyClipboardHelpers = function(config) {
            var
                clip,
                clips = $jq("#mfWidgets").data('zeroClipboard');
            if (clips !== undefined) {
                while (clips.length > 0)
                {
                    clip = clips.pop();
                    clip.destroy();
                }
            }
        },

        // Sets value of a selector based upon a url param.
        _setSelectorValueFromURLParam = function (selectorID, urlParam) {
            var
                text = $mf.uiUtils.getURLParam(urlParam);
            if (text != undefined) {
                _setSelectorValueFromText(selectorID, text);
            }
        },

        // Sets value of a selector based upon a text string.
        _setSelectorValueFromText = function (selectorID, text) {
            var
                jqSelector = 'select#' + selectorID + ' option';
            $jq(jqSelector).each(function () {
                this.selected = (this.text.toUpperCase() == text.toUpperCase());
            });
        };

    // Register widget so that it is visible.
    $mf.registerWidget({
        id : 'uiUtils',
        createClipboardHelper : _createClipboardHelper,
        destroyClipboardHelpers : _destroyClipboardHelpers,
        doComboBoxRefill : _doComboBoxRefill,
        doComboBoxFill : _doComboBoxRefill,
        doComboBoxCascade : _doComboBoxCascade,
        getFormAsJSON : _getFormAsJSON,
        getFormAsString : _getFormAsString,
        setFormLockedState : _setFormLockedState,
        setFormChangedHandler : _setFormChangedHandler,
        setFormTabIndexes : _setFormTabIndexes,
        setValueOfInput : _setValueOfInput,
        setValueOfInputCollection : _setValueOfInputCollection,
        setSelectorValueFromText : _setSelectorValueFromText,
        setSelectorValueFromURLParam : _setSelectorValueFromURLParam,
        openURL : _openURL,
        postToURL : _postToURL,
        getDate : _getDate,
        setDate : _setDate,
        getFileExtension : _getFileExtension,
        validateFileForUpload : _validateFileForUpload,
        getURLParam : _getURLParam
    });
}());