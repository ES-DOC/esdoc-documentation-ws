// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: EntityManager :: Manages entity details viewing & editing.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    var
        // The collection of entity managers.
        _managers = [],

        // Retrieves a manager of matching type.
        _get = function (entityType) {
            var
                i,
                controller;
            for (i = 0; i < _managers.length; i++) {
                controller = _managers[i];
                if (controller.info.entityType === entityType) {
                    return controller;
                }
            }
            return undefined;
        },

        // Factory method to create an entity manager.
        _create = function (spec) {
            // Validate spec.
            if (spec === undefined ||
                spec.entityType === undefined ||
                spec.displayName === undefined ||
                spec.dialogConfig === undefined ||
                spec.dialogConfig.width === undefined) {
                throw {
                    name : 'EntityManagerFactoryError',
                    message : 'The entity controller specification is invalid.'
                };
            }

            // Private members.
            var
                // Entity information.
                _info = {
                    // Type of entity being managed.
                    entityType : spec.entityType,

                    // Initialisation flag.
                    isInitialised : false,

                    // State change flag.
                    hasInstanceChanged : false,

                    // The entity instance loaded from server.
                    instance : undefined,

                    // Collection loading flag.
                    isCollectionBeingLoaded : false,

                    // The entity instance loaded from server.
                    instanceAsJSON : function () {
                        return JSON.stringify(_info.instance);
                    },

                    // Sets instance.
                    setInstance : function (instance) {
                        _info.instance = instance;
                        if (instance.ID === 0) {
                            _events.onEntityCreated.publish();

                        } else {
                            _events.onEntityLoaded.publish();
                        }
                    },

                    // Resets information content.
                    reset : function () {
                        _info.hasInstanceChanged = false;
                        _info.instance = undefined;
                        _info.isCollectionBeingLoaded = false;
                    }
                },

                // User interface specific information/behaviour.
                _ui = {
                    // The jquery selectors in use by this widget.
                    jqSelectors : {
                        container : '#mfEntity_' + spec.entityType,
                        form : '#mfEntity_' + spec.entityType + ' .mf-entity-form-container' + ' form',
                        formContainer : '#mfEntity_' + spec.entityType + ' .mf-entity-form-container',
                        forButton : function (buttonType) {
                            var
                                result = '#mfEntity_' + spec.entityType + ' .mf-entity-form-toolbar ';
                            if (buttonType === 'close') {
                                result += '.mf-entity-form-button-close';
                            }
                            else if (buttonType === 'delete') {
                                result += '.mf-entity-form-button-delete';
                            }
                            else if (buttonType === 'save') {
                                result += '.mf-entity-form-button-save';
                            }
                            else if (buttonType === 'saveclose') {
                                result += '.mf-entity-form-button-save-close';
                            }
                            return result;
                        }
                    },

                    // The resources used during various operations.
                    resources : {
                        // Title used in dialogs.
                        title : spec.displayName,

                        // Title to be displayed in modal dialog.
                        dialogTitle : spec.displayName,

                        // Derives dialog title from controller action.
                        getDialogCaption : function (prefix, suffix) {
                            var
                                result = _ui.resources.dialogTitle;
                            if (prefix !== undefined) {
                                result = prefix + result;
                            }
                            if (suffix !== undefined) {
                                result = result + suffix;
                            }
                            return result;
                        },

                        // Confirms entity deletion.
                        deleteComfirmation : "Do you really want to delete this item ?",

                        // Displayed when entity has been successfully deleted.
                        deleteSuccess : "The item was successfully deleted.",

                        // Displayed whilst deleting an entity.
                        deleteProgress : "Deleting item",

                        // Validation errors.
                        validationErrors : "Please correct validation errors.",

                        // Displayed whilst saving entity changes.
                        saveProgress : "Saving details",

                        // Displayed when entity changes have been successfully changed.
                        saveSuccess : "Details have been successfully saved.",

                        // Displayed when closing whilst changes are outstanding.
                        closeConfirmation : "Your changes will be lost ... do you really want to proceed ?",

                        // Displayed when a server side error has occurred.
                        errorCaption : 'Server Side Error',

                        // Displayed when a server side error has occurred.
                        errorMessage : 'An error occurred whilst processing the entity request.  Please contact system administrator if this continues.'
                    },

                    // Information for rendering modal dialog.
                    dialogConfig : spec.dialogConfig,

                    // The associated ui.toolbar.
                    toolbar : {
                        // Initialises the toolbar buttons.
                        initialise : function () {
                            var
                                render = function (type, icon, action) {
                                    $jq(_ui.jqSelectors.forButton(type)).button({
                                        icons : {
                                            primary : icon
                                        },
                                        text : true
                                    }).bind('click', action);
                                };
                            render('close', 'ui-icon-circle-close', _actions.close);
                            render('delete', 'ui-icon-trash', _actions.deleteInstance);
                            render('save', 'ui-icon-disk', _actions.save);
                            render('saveclose', 'ui-icon-refresh', _actions.saveAndClose);
                        }
                    },

                    // The associated HXTML form with which the entity details are displayed / edited.
                    form : (function () {
                        var
                            // Flag indicating whether form data has changed.
                            _hasChanged = false,

                            // Flag indicating whether form data changes are to be abandoned.
                            _abandonChanges = false,

                            // Confirms closure of the form.
                            _confirmClose = function () {
                                var
                                    onCloseConfirmed = function () {
                                        _abandonChanges = true;
                                        $jq(_ui.jqSelectors.container).dialog('close');
                                    },
                                    messageInfo = {
                                        type : $mf.feedback.MESSAGE_TYPE_CONFIRMATION,
                                        caption : _ui.resources.dialogTitle,
                                        text : _ui.resources.closeConfirmation,
                                        continuation : onCloseConfirmed
                                    };
                                $mf.feedback.showMessage(messageInfo);
                            },

                            // Sets state of form button.
                            _setButtonState = function (type, state) {
                                $jq(_ui.jqSelectors.forButton(type)).button({disabled: !state});
                            };

                        return {
                            // Resets form change status.
                            resetChangeStatus : function () {
                                _hasChanged = false;
                                _abandonChanges = false;
                            },

                            // Resets form values.
                            reset : function () {
                                $jq(_ui.jqSelectors.form)[0].reset();
                                _ui.form.resetChangeStatus();
                                _events.onFormReset.publish();
                            },

                            // Gets form's change status.'
                            getHasChanged : function () {
                                return _hasChanged;
                            },

                            // Sets form's change status.'
                            setHasChanged : function (status) {
                                _hasChanged = status;
                            },

                            // Resets form values.
                            close : function () {
                                $jq(_ui.jqSelectors.container).dialog('close');
                            },

                            // Initialises form as a modal dialog.
                            initialise : function () {
                                var
                                    dialogConfig = {
                                        autoOpen: false,
                                        width: _ui.dialogConfig.width,
                                        position: ['center', 100],
                                        resizable: false,
                                        modal: true,
                                        close: function() {
                                            _ui.form.reset();
                                            _events.onFormClosed.publish();
                                            _info.reset();
                                        },
                                        beforeclose: function() {
                                            var
                                                canClose = false;
                                            if (_hasChanged === false || _abandonChanges === true) {
                                                canClose = true;
                                                _events.onFormClosing.publish();
                                            } else {
                                                _confirmClose();
                                            }
                                            return canClose;
                                        }
                                    };
                                $jq(_ui.jqSelectors.container).dialog(dialogConfig);
                            },

                            // Loads form from server.
                            load : function () {
                                var
                                    // Callback to handle get form load success event.
                                    onSuccess = function (xhtml) {
                                        $jq(_ui.jqSelectors.formContainer).html(xhtml);
                                        $mf.uiUtils.setFormChangedHandler(_ui.jqSelectors.form, function () {
                                            _hasChanged = true;
                                            _setButtonState('save', true);
                                            _setButtonState('saveclose', true);
                                        });
                                        _events.onFormLoaded.publish();
                                        _events.onFormReady.publish();
                                        $jq(_ui.jqSelectors.form).validate({
                                            errorClass : 'mf-field-invalid',
                                            validClass : 'mf-field-valid'
                                        });
                                    };
                                $mf.repository.getEntityDetailForm(_info.entityType, onSuccess, _events.onError.publish)
                            },

                            // Sets dialog caption.
                            setCaption : function (action) {
                                $jq(_ui.jqSelectors.container).dialog('option', 'title', action + ' ' + _ui.resources.title);
                            },

                            // Displays the ui.form.
                            display : function (action) {
                                var
                                    validator;
                                // Reset validators.
                                validator = $jq(_ui.jqSelectors.form).validate();
                                if (validator !== undefined) {
                                    validator.resetForm();
                                }
                                // Set ui state.
                                if (action === "Edit") {
                                    $mf.uiUtils.setFormLockedState(_ui.jqSelectors.form, false);
                                    _setButtonState('close', true);
                                    _setButtonState('delete', true);
                                    _setButtonState('save', false);
                                    _setButtonState('saveclose', false);
                                } else if (action === "Create") {
                                    $mf.uiUtils.setFormLockedState(_ui.jqSelectors.form, false);
                                    _setButtonState('close', true);
                                    _setButtonState('delete', false);
                                    _setButtonState('save', false);
                                    _setButtonState('saveclose', false);
                                } else if (action === "View") {
                                    $mf.uiUtils.setFormLockedState(_ui.jqSelectors.form, true);
                                    _setButtonState('close', true);
                                    _setButtonState('delete', false);
                                    _setButtonState('save', false);
                                    _setButtonState('saveclose', false);
                                }
                                // Open dialog.
                                _ui.form.setCaption(action);
                                $jq(_ui.jqSelectors.container).dialog('open');
                            }
                        }
                    }())
                },

                // Event publishers.
                _events = {
                    // Event raised when entity manager has been initialised.
                    onInitialisation : $mf.createEventPublisher(),

                    // Event raised when an entity is about to be deleted.
                    onEntityDeleting : $mf.createEventPublisher(),

                    // Event raised when an entity has been deleted.
                    onEntityDeleted : $mf.createEventPublisher(),

                    // Event raised when an entity has been deleted and the message displayed to user.
                    onEntityDeletedMessageDisplayed : $mf.createEventPublisher(),

                    // Event raised when entity changes are about to be saved.
                    onEntitySaving : $mf.createEventPublisher(),

                    // Event raised when entity changes have been saved.
                    onEntitySaved : $mf.createEventPublisher(),

                    // Event raised when an entity has been saved and the message displayed to user.
                    onEntitySavedMessageDisplayed : $mf.createEventPublisher(),

                    // Event raised when entity is about to be loaded.
                    onEntityLoading : $mf.createEventPublisher(),

                    // Event raised when entity has been loaded.
                    onEntityLoaded : $mf.createEventPublisher(),

                    // Event raised when entity collection is about to be loaded.
                    onEntityCollectionLoading : $mf.createEventPublisher(),

                    // Event raised when entity collection has been refreshed.
                    onEntityCollectionRefreshed : $mf.createEventPublisher(),

                    // Event raised when entity has been created.
                    onEntityCreated : $mf.createEventPublisher(),

                    // Event raised when a processing error has occurred.
                    onError : $mf.createEventPublisher(),

                    // Event raised when entity form is closed.
                    onFormClosing : $mf.createEventPublisher(),

                    // Event raised when entity form is closed.
                    onFormClosed : $mf.createEventPublisher(),

                    // Event raised when entity form has been opened.
                    onFormOpened : $mf.createEventPublisher(),

                    // Event raised when entity form is reset.
                    onFormReset : $mf.createEventPublisher(),

                    // Event raised when entity form has been loaded.
                    onFormLoaded: $mf.createEventPublisher(),

                    // Event raised when entity form us ready to use.
                    onFormReady: $mf.createEventPublisher(),

                    // Standard initialisation routine.
                    initialise : function () {
                        this.onError.bind( function () {
                            var
                                messageInfo = {
                                    type : $mf.feedback.MESSAGE_TYPE_ERROR,
                                    caption : _ui.resources.errorCaption,
                                    text : _ui.resources.errorMessage
                                };
                            $mf.feedback.showMessage(messageInfo);
                        });
                        this.onInitialisation.bind( function () {
                            _info.isInitialised = true;
                        });
                        this.onEntityDeleting.bind( function () {
                            $mf.feedback.showProgress(_ui.resources.deleteProgress);
                        });
                        this.onEntityDeleted.bind( function () {
                            var
                                messageInfo = {
                                    type : $mf.feedback.MESSAGE_TYPE_INFORMATION,
                                    caption : _ui.resources.getDialogCaption('Delete ', undefined),
                                    text : _ui.resources.deleteSuccess,
                                    continuation : _events.onEntityDeletedMessageDisplayed.publish
                                };
                            _ui.form.close();
                            $mf.feedback.showMessage(messageInfo);
                        });
                        this.onFormOpened.bind( function () {
                            _ui.form.setHasChanged(false);
                        });
                        this.onEntitySaving.bind( function () {
                            $mf.feedback.showProgress(_ui.resources.saveProgress);
                        });
                        this.onEntitySaved.bind( function (data) {
                            var
                                messageInfo = {
                                    type : $mf.feedback.MESSAGE_TYPE_INFORMATION,
                                    caption : _ui.resources.getDialogCaption('Save ', undefined),
                                    text : _ui.resources.saveSuccess,
                                    continuation : _events.onEntitySavedMessageDisplayed.publish
                                };
                            _info.hasInstanceChanged = true;
                            if (_info.instance.ID === 0) {
                                _info.instance.ID = data.entityID;
                                _ui.form.setCaption('Edit');
                            }
                            _ui.form.resetChangeStatus();
                            $mf.feedback.showMessage(messageInfo);
                        });
                    }
                },

                // Entity actions.
                _actions = (function () {
                    var
                        // Opens entity form in relevant mode.
                        _open = function (action, id) {
                            var
                                onRetrieveSuccess = function (instance) {
                                    _info.setInstance(instance);
                                    $mf.feedback.hideProgress();
                                    _ui.form.display(action);
                                    _events.onFormOpened.publish(action);
                                };
                            _events.onEntityLoading.publish();
                            if (action === "Create") {
                                _info.setInstance({ID : 0});
                                _ui.form.display(action);
                                _events.onFormOpened.publish(action);
                            } else {
                                $mf.repository.getEntity(_info.entityType, id, onRetrieveSuccess, _events.onError.publish);
                            }
                        };

                    return {
                        // Standard initialisation routine.
                        initialise : function (continuation) {
                            if (_info.isInitialised !== true) {
                                _events.initialise();
                                _ui.toolbar.initialise();
                                _ui.form.initialise();
                                _ui.form.load();
                                _events.onInitialisation.publish();
                            }
                            if ($jq.isFunction(continuation)) {
                                continuation();
                            }
                        },

                        // Opens in edit mode.
                        openForEdit : function (id) {
                            _actions.initialise(function () {
                                _open("Edit", id);
                            });
                        },

                        // Opens in view mode.
                        openForView : function (id) {
                            _actions.initialise(function () {
                                _open("View", id);
                            });
                        },

                        // Opens in create mode.
                        openForCreate : function () {
                            _actions.initialise(function () {
                                _open("Create");
                            });
                        },

                        // Deletes entity.
                        deleteInstance : function () {
                            var
                                doDelete = function () {
                                    _events.onEntityDeleting.publish();
                                    $mf.repository.deleteEntity(_info.entityType, _info.instance.ID, _events.onEntityDeleted.publish, _events.onError.publish);
                                },
                                messageInfo = {
                                    type : $mf.feedback.MESSAGE_TYPE_CONFIRMATION_WARNING,
                                    caption : _ui.resources.getDialogCaption('Delete ', undefined),
                                    text : _ui.resources.deleteComfirmation,
                                    continuation : doDelete
                                };
                            $mf.feedback.showMessage(messageInfo);
                        },

                        // Deletes entity by id.
                        deleteByID : function (id) {
                            var
                                doDelete = function () {
                                    _events.onEntityDeleting.publish();
                                    $mf.repository.deleteEntity(
                                        _info.entityType,
                                        id,
                                        _events.onEntityDeleted.publish,
                                        _events.onError.publish);
                                },
                                messageInfo = {
                                    type : $mf.feedback.MESSAGE_TYPE_CONFIRMATION_WARNING,
                                    caption : _ui.resources.getDialogCaption('Delete ', undefined),
                                    text : _ui.resources.deleteComfirmation,
                                    continuation : doDelete
                                };
                            $mf.feedback.showMessage(messageInfo);
                        },

                        //  Saves changes to repository.
                        save : function (continuation) {
                            var
                                doContinuation = function () {
                                    if ($jq.isFunction(continuation)) {
                                        continuation();
                                    }
                                },
                                onSaveSuccess = function (data) {
                                    _events.onEntitySaved.publish(data);
                                    doContinuation(data);
                                },
                                messageInfo;
                            if (_ui.form.getHasChanged() === false) {
                                doContinuation();
                            } else {
                                // Invalid forms.
                                if ($jq(_ui.jqSelectors.form).valid() === false) {
                                    messageInfo = {
                                        type : $mf.feedback.MESSAGE_TYPE_VALIDATION,
                                        caption : _ui.resources.getDialogCaption(undefined, ' - Validation Errors'),
                                        text : _ui.resources.validationErrors
                                    };
                                    $mf.feedback.showMessage(messageInfo);
                                // Valid forms.
                                } else {
                                    _events.onEntitySaving.publish();
                                    $mf.repository.saveEntity(_info.entityType, _info.instance.ID, _info.instanceAsJSON, onSaveSuccess, _events.onError.publish);
                                }
                            }
                        },

                        //  Saves changes to repository & closes ui.form.
                        saveAndClose : function () {
                            _actions.save(_actions.close);
                        },

                        //  Closes ui.form immediately.
                        close : function () {
                            _ui.form.close();
                        },

                        // Loads the collection of entities.
                        loadCollection : function () {
                            var
                                onCollectionLoaded = function (collection) {
                                    _events.onEntityCollectionRefreshed.publish(collection);
                                };
                            if (_info.isCollectionBeingLoaded === false) {
                                _info.isCollectionBeingLoaded = true;
                                _events.onEntityCollectionLoading.publish();
                                $mf.repository.getEntityCollection(_info.entityType, onCollectionLoaded, _events.onError.publish);
                            }
                        }
                    }
                }()),

                // Instantiate, store & return.
                newEntityManager = {
                    info : _info,
                    events : _events,
                    actions : _actions
                };
            _managers.push(newEntityManager);
            return newEntityManager;
        },

        // Invokes an action on an entity controller.
        _invokeAction = function (entityType, entityID, action) {
            var
                controller = _get(entityType);
            if (controller !== undefined) {
                controller.actions[action](entityID);
            }
        },

        // Deletes an entity instance.
        _deleteEntity = function (entityType, entityID) {
            _invokeAction(entityType, entityID, "deleteByID");
        },

        // Displays an entity in view mode.
        _viewEntity = function (entityType, entityID) {
            _invokeAction(entityType, entityID, "openForView");
        },

        // Displays an entity in edit mode.
        _editEntity = function (entityType, entityID) {
            _invokeAction(entityType, entityID, "openForEdit");
        },

        // Displays an entity in create mode.
        _createEntity = function (entityType, entityID) {
            _invokeAction(entityType, entityID, "openForCreate");
        };

    // Register widget so that it is visible.
    $mf.registerWidget({
        id : 'entityManager',
        create : _create,
        get : _get,
        deleteEntity : _deleteEntity,
        viewEntity : _viewEntity,
        editEntity : _editEntity,
        createEntity : _createEntity
    });

}());