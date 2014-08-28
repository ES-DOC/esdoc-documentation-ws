// ECMAScript 5 Strict Mode
"use strict";

//// --------------------------------------------------------
// $jq :: JQuery nonconflict reference.
// See :: http://www.tvidesign.co.uk/blog/improve-your-jquery-25-excellent-tips.aspx#tip19
// --------------------------------------------------------
window.$ = window.$jq = jQuery.noConflict();

//// --------------------------------------------------------
// $mf :: Top level Prodiguer javascript container.
// N.B. Declared in a functional closure so as not to pollute global namespace.
// --------------------------------------------------------
window.$mf = (function () {
    // Private members.
    var
        // Application related constants.
        APP_NAME = 'Metafor CIM',
        APP_VERSION = '1_0rc1',

        // The jquery selectors in use by this widget.
        jqSelectors = {
            siteHeaderMenuItems : ".mf-menu ui li a",
            siteFooterMenuItems : ".mf-footer-menu ul li a",
            siteLinks : "a[rel=external]"
        },

        // Manages widgets used within the application.
        widgetManager = (function () {
            // Private members.
            var
                // The collection of widgets plugged into the site.
                widgets = [],

                // Returns a widget from managed collection.
                get = function (id) {
                    var result, i;
                    for (i = 0; i < widgets.length; i++) {
                        if (widgets[i].id === id) {
                            result = widgets[i];
                            break;
                        }
                    }
                    return result;
                },

                // Registers a widget with the collection.
                register = function (newWidget) {
                    if (get(newWidget.id) === undefined) {
                        widgets.push(newWidget);
                        $mf[newWidget.id] = newWidget;
                    }
                },

                // Initialise registered widgets.
                initialise = function () {
                    var i;
                    for (i = 0; i < widgets.length; i++) {
                        if (widgets[i].initialise !== undefined) {
                            widgets[i].initialise();
                        }
                    }
                };

            // Public members.
            return {
                register : register,
                get : get,
                initialise : initialise
            };
        }()),

        // Renders the UI upon initialisation.
        renderUI = function () {
            $jq(jqSelectors.siteHeaderMenuItems).addClass('ui-corner-all');
            $jq(jqSelectors.siteFooterMenuItems).addClass('ui-corner-all');
            $jq(jqSelectors.siteLinks).attr('target', '_blank');
        },

        // Creates an event publisher.
        createEventPublisher = function () {
            var
                // Collection of event handlers,
                _handlers = [];

            return {
                // Publishes event by invoking registered handlers.
                publish : function (eventData) {
                    var
                        i,
                        handler;
                    for (i = 0; i < _handlers.length; i++) {
                        handler = _handlers[i];
                        handler(eventData);
                    }
                },

                // Adds a handler to managed collection.
                bind : function ( handler ) {
                    _handlers.push(handler);
                },

                // Collection of event handlers,
                handlers : _handlers
            }
        },

        // Renders site footer.
        renderSitefooter = function () {
            var
                config = {classmodifier : 'mf-site-footer-',
                           showclose: true,
                           closebutton : "[hide]&nbsp;&nbsp;&nbsp;&nbsp;"};
            $jq(".mf-site-footer-container").constantfooter(config);
        };

    // Public members.
    return {
        app : {
            name : APP_NAME,
            version : APP_VERSION
        },

        // Registers a widget with the managed collection.
        registerWidget : widgetManager.register,

        // Renders site footer.
        renderSitefooter : renderSitefooter,

        // Creates an event publisher helper.
        createEventPublisher : createEventPublisher,

        // Standard initialisation routine.
        initialise : function () {
            widgetManager.initialise();
            renderUI();
            renderSitefooter();
        }
    };
}());

// Initialise when the page is loaded.
$jq(document).ready(function() {
    window.$mf.initialise();
});