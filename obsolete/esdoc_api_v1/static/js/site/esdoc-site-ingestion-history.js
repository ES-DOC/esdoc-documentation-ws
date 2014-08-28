// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Ingest History.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    var
        // JQuery selectors in use across this class.
        jqSelectors = {
            dt : ".mf-datatable"           
        },

        // Search result column references.
        cols = {
            Institute : 0,
            IngestSource : 1,
            IngestURL : 2,
            IngestStartDate : 3,
            IngestCount : 4,
            IngestState : 5
        },

        // Data table configuration.
        createDataTableConfig = function () {
            var
                config = $mf.grid.createConfigInfo();
            config.aoColumnDefs = [
                {sType: 'date', aTargets: [ cols.IngestStartDate ]},
                {sWidth: "80px", aTargets: [ cols.IngestCount ]},
                {sWidth: "100px", aTargets: [ cols.Institute ]},
                {sWidth: "110px", aTargets: [ cols.IngestState ]},
                {sWidth: "140px", aTargets: [ cols.IngestStartDate ]},
                {sWidth: "200px", aTargets: [ cols.IngestSource ]},
                {sWidth: "400px", aTargets: [ cols.IngestURL ]}
            ];
            return config;
        },

        // Standard initialisation routine.
        initialise = function () {
            $mf.grid.render(jqSelectors.dt, createDataTableConfig());
        };

    // Document ready event handler.
    $jq(document).ready(function() {
        initialise();
    });
}());