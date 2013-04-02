// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: Validator :: Manages the process of validating user input.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    var
        // Standard initialisation routine.
        _initialise = function() {
            // Set standard messages.
            $jq.validator.messages.required = "Required Field";
            $jq.validator.messages.email = "Invalid Email";
            $jq.validator.messages.url = "Invalid URL";
            $jq.validator.messages.date = "Invalid date.";
            $jq.validator.messages.dateISO = "Invalid date.";
            $jq.validator.messages.number = "Invalid number";
            $jq.validator.messages.digits = "Enter only digits";
            $jq.validator.messages.equalTo = "Enter same value again";
            $jq.validator.messages.accept = "Invalid extension";
            $jq.validator.messages.maxlength = $.validator.format("Do not enter more than {0} characters");
            $jq.validator.messages.minlength = $.validator.format("Enter at least {0} characters");
            $jq.validator.messages.rangelength = $.validator.format("Enter a value between {0} and {1} characters long");
            $jq.validator.messages.range = $.validator.format("Enter a value between {0} and {1}");
            $jq.validator.messages.max = $.validator.format("Enter a value less than or equal to {0}");
            $jq.validator.messages.min = $.validator.format("Enter a value greater than or equal to {0}");

            // Set standard rules.
            $jq.validator.addClassRules({
                'mf-rule-required': {
                    required: true
                },
                'mf-rule-email': {
                    email: true
                },
                'mf-rule-url': {
                    url: true
                },
                'mf-rule-date-iso': {
                    dateISO: true
                },
                'mf-rule-number': {
                    number: true
                },
                'mf-rule-digits': {
                    digits: true
                },
                'mf-rule-equal-to': {
                    equalTo: true
                },
                'mf-rule-accept': {
                    accept: true
                },
                'mf-rule-maxlength': {
                    maxlength: true
                },
                'mf-rule-minlength': {
                    minlength: true
                },
                'mf-rule-rangelength': {
                    rangelength: true
                },
                'mf-rule-range': {
                    range: true
                },
                'mf-rule-max': {
                    max: true
                },
                'mf-rule-min': {
                    min: true
                }
            });
        };

    // Register the widget and it's public members.
    $mf.registerWidget({
        id : 'validator',
        initialise : _initialise
    });
}());