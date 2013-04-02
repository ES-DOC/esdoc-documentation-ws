// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Search controller :: Basic.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
// --------------------------------------------------------
(function () {
    // Create search engine.
    var se = $mf.searchEngine.create({
        searchType : 'Basic',
        autoBegin : false,
        renderDataTable : false
    });

    // JSON data returned from server.
    var json = undefined;

    // Metadata regarding tabs on page.
    var tabs = [
        { id : 0,
          key : 'Experiments',
          count : 0,
          text : '',
          div : '#mfSearchResultExperiments',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultExperiments table'},
        { id : 1,
          key : 'Models',
          count : 0,
          text : '',
          div : '#mfSearchResultModels',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultModels table'},
        { id : 2,
          key : 'Simulations',
          count : 0,
          text : '',
          div : '#mfSearchResultSimulations',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultSimulations table'},
        { id : 3,
          key : 'Ensembles',
          count : 0,
          text : '',
          div : '#mfSearchResultEnsembles',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultEnsembles table'},
        { id : 4,
          key : 'Grids',
          count : 0,
          text : '',
          div : '#mfSearchResultGrids',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultGrids table'},
        { id : 5,
          key : 'Platforms',
          count : 0,
          text : '',
          div : '#mfSearchResultPlatforms',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultPlatforms table'},
        { id : 6,
          key : 'Data',
          count : 0,
          text : '',
          div : '#mfSearchResultData',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultData table'},
        { id : 7,
          key : 'Quality',
          count : 0,
          text : '',
          div : '#mfSearchResultQuality',
          dt : undefined,
          dtConfig : undefined,
          dtTable : '#mfSearchResultQuality table'},
    ];

    // Currently active tab.
    var activeTab = tabs[0];

    // JQuery tabs plugin wrapper.
    var $tabs = undefined;

    // Sets active tab based upon passed key.
    var setActiveTab = function (key) {
        activeTab = _(tabs).detect(function (t) {
            return t.key === key;
        });
    };

    // Displays currently active tab.
    var displayActiveTab = function () {
        $tabs.tabs('select', activeTab.id);
        $jq(activeTab.div).show();
        activeTab.dt = $mf.grid.render(activeTab.dtTable, activeTab.dtConfig);
    };

    // Opens a selected CIM instance using passed url.
    var openCimURL = function(url, id, version) {
        url = url.replace('{id}', id);
        url = url.replace('{version}', version);
        $mf.uiUtils.openURL(url, true);
    };

    // Opens a selected CIM instance using passed url.
    var openCimInstance = function(row) {
        var position = activeTab.dt.fnGetPosition(row);
        var data = activeTab.dt.fnGetData(position);
        var urlType = data[data.length - 3];
        var cimID =  data[data.length - 2];
        var cimVersion =  data[data.length - 1];
        var url = urlType === 'viewer' ? 
            '/site/public/tools/viewer/integrated/1.5/en/{id}/{version}' :
            '/api/rest/documents/1.5/en/{id}/{version}';
        openCimURL(url, cimID, cimVersion);
    };

    // Datatables config - Experiments.
    var setDatatableConfigForExperiments = function () {
        // Data-table columns.
        var
            dtCols = {
                CimProject : 0,
                ShortName : 1,
                LongName : 2,
                CimVersion : 3,
                FunctionOpenXML : 4,
                FunctionOpenJSON : 5,
                CimDefaultURL : 6,
                CimID : 7,
                CimVersionHidden : 8
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "60px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]},
                    {sWidth: "160px", aTargets: [ dtCols.ShortName ]}
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[0].dtConfig = config;
    };

    // Datatables config - Models.
    var setDatatableConfigForModels = function () {
        // Data-table columns.
        var dtCols = {
                CimProject : 0,
                ShortName : 1,
                LongName : 2,
                Date : 3,
                CimVersion : 4,
                FunctionOpenXML : 5,
                FunctionOpenJSON : 6,
                CimDefaultURL : 7,
                CimID : 8,
                CimVersionHidden : 9
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    dateCols = [
                        dtCols.Date
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sType: 'date', aTargets: dateCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "60px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "100px", aTargets: [ dtCols.Date ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]},
                    {sWidth: "160px", aTargets: [ dtCols.ShortName ]},
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[1].dtConfig = config;
    };

    // Datatables config - Simulations.
    var setDatatableConfigForSimulations = function () {
        // Data-table columns.
        var
            dtCols = {
                CimProject : 0,
                ShortName : 1,
                LongName : 2,
                CimVersion : 3,
                FunctionOpenXML : 4,
                FunctionOpenJSON : 5,
                CimDefaultURL : 6,
                CimID : 7,
                CimVersionHidden : 8
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "60px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]},
                    {sWidth: "250px", aTargets: [ dtCols.ShortName ]}
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[2].dtConfig = config;
    };

    // Datatables config - Ensembles.
    var setDatatableConfigForEnsembles = function () {
        // Data-table columns.
        var
            dtCols = {
                CimProject : 0,
                Experiment : 1,
                ShortName : 2,
                LongName : 3,
                CimVersion : 4,
                FunctionOpenXML : 5,
                FunctionOpenJSON : 6,
                CimDefaultURL : 7,
                CimID : 8,
                CimVersionHidden : 9
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "60px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]},
                    {sWidth: "160px", aTargets: [ dtCols.ShortName, dtCols.Experiment ]}
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[3].dtConfig = config;
    };

    // Datatables config - Grids.
    var setDatatableConfigForGrids = function () {
        // Data-table columns.
        var
            dtCols = {
                CimProject : 0,
                ShortName : 1,
                LongName : 2,
                CimVersion : 3,
                FunctionOpenXML : 4,
                FunctionOpenJSON : 5,
                CimDefaultURL : 6,
                CimID : 7,
                CimVersionHidden : 8
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "60px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]},
                    {sWidth: "160px", aTargets: [ dtCols.ShortName ]}
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[4].dtConfig = config;
    };

    // Datatables config - Platforms.
    var setDatatableConfigForPlatforms = function () {
        // Data-table columns.
        var
            dtCols = {
                CimProject : 0,
                ShortName : 1,
                LongName : 2,
                CimVersion : 3,
                FunctionOpenXML : 4,
                FunctionOpenJSON : 5,
                CimDefaultURL : 6,
                CimID : 7,
                CimVersionHidden : 8
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "160px", aTargets: [ dtCols.ShortName ]}
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[5].dtConfig = config;
    };

    // Datatables config - Data.
    var setDatatableConfigForData = function () {
        // Data-table columns.
        var
            dtCols = {
                CimProject : 0,
                Acronym : 1,
                CimVersion : 2,
                FunctionOpenXML : 3,
                FunctionOpenJSON : 4,
                CimDefaultURL : 5,
                CimID : 6,
                CimVersionHidden : 7
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "60px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]}
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[6].dtConfig = config;
    };

    // Datatables config - Data.
    var setDatatableConfigForQuality = function () {
        // Data-table columns.
        var
            dtCols = {
                CimProject : 0,
                Acronym : 1,
                CimVersion : 2,
                FunctionOpenXML : 3,
                FunctionOpenJSON : 4,
                CimDefaultURL : 5,
                CimID : 6,
                CimVersionHidden : 7
            };
        // Data-table configuration.
        var
            config = (function () {
                var
                    hiddenCols = [
                        dtCols.CimID,
                        dtCols.CimVersionHidden,
                        dtCols.CimDefaultURL
                    ],
                    nonSortableCols = [
                        dtCols.CimProject,
                        dtCols.FunctionOpenXML,
                        dtCols.FunctionOpenJSON,
                        dtCols.CimVersion
                    ],
                    config = $mf.grid.createConfigInfo();
                config.aoColumnDefs = [
                    {bVisible : false, aTargets : hiddenCols},
                    {bSortable : false, aTargets : nonSortableCols},
                    {sWidth: "24px", aTargets: [ dtCols.FunctionOpenXML, dtCols.FunctionOpenJSON ]},
                    {sWidth: "60px", aTargets: [ dtCols.CimVersion ]},
                    {sWidth: "100px", aTargets: [ dtCols.CimProject ]}
                ];
                return config;
            }());
        // Associate tab with config.
        tabs[7].dtConfig = config;
    };

    // Criteria loaded event handler.
    se.events.onCriteriaInitialising.bind(function () {
        if ($tabs === undefined) {
            $tabs = $jq("#mfSearch_BasicTabs").tabs();   // Jquery tabs widget.
        }        
        $jq("#mfSearch_BasicTabs ul li a").bind('click', function () {
            $jq(activeTab.div).toggle();
            setActiveTab(this.id.replace('mfSearchResultTab', ''));
            displayActiveTab();
        });
        setDatatableConfigForData();
        setDatatableConfigForExperiments();
        setDatatableConfigForModels();
        setDatatableConfigForSimulations();
        setDatatableConfigForPlatforms();
        setDatatableConfigForGrids();
        setDatatableConfigForEnsembles();
        setDatatableConfigForQuality();
    });

    // Search results assigned event handler.
    se.events.onResultsAssigned.bind(function () {
        var tab;
        var nonZeroTabs = [];
        
        // Loop tabs and re-assign text and count.
        _.each(tabs, function(tab) {
            // Set tab count.
            tab.count = $jq('.mf-search-result-' + tab.key.toLowerCase()).length;
            if (tab.count > 0) {
                nonZeroTabs.push(tab);
            }
            // Set tab text.
            tab.text = tab.key;
            tab.text += ' (';
            tab.text += tab.count.toString();
            if (tab.count == 150) {
                tab.text += '+';
            }
            tab.text += ')';
            $jq('#mfSearchResultTab' + tab.key).text(tab.text);
        });

        // If there is only a single tab with data set it to be the active one.
        if (nonZeroTabs.length === 1) {
            activeTab = nonZeroTabs[0];
        }

        // Activate current tab.
        displayActiveTab();

        // Event handler for row click event.
        $jq(".mf-datatable-info-cell").bind('click', function () {
            var row = $jq(this).parent()[0];
            openCimInstance(row);
        });
    });

    // Document ready event handler.
    $jq(document).ready(function() {
        se.actions.begin();
    });
}());