// ECMAScript 5 Strict Mode
"use strict";

// --------------------------------------------------------
// Widget :: Grid :: Manages the process of displaying data grids.
// N.B. Declared in a self-invoking functional closure so as
//      not to pollute global namespace.
//      Uses the JQuery plugin: http://www.datatables.net
// --------------------------------------------------------
(function () {
    var
        // The managed collection of datatables.
        _dtCollection = [],

        // Registers a data-table with managed collection.
        _setDataTable = function ( dtSelector ) {
            var
                dt = {
                    selector : dtSelector,
                    grid : undefined,
                    config : undefined,
                    colFilters : {
                        filters : [],
                        set : function ( col, colsRelated, source, sourceNull ) {
                            var
                                colInfo = {
                                    col : col,
                                    related : colsRelated,
                                    sourceValue : function () {
                                        var
                                            result = $jq(source).val();
                                        return result === sourceNull ? '' : result;
                                    }
                                };
                             this.filters.push(colInfo);
                        },
                        get : function ( col ) {
                            var
                                i, result, f;
                            for (i = 0; i < this.filters.length; i++) {
                                f = this.filters[i];
                                if (f.col === col) {
                                    result = f;
                                    break;
                                }
                            }
                            return result;
                        }
                    }
                };
            _dtCollection.push(dt);
            return dt;
        },

        // Gets first matching data table from managed collection.
        _getDataTable = function ( dtSelector ) {
            var
                i, dt;
            for (i = 0; i < _dtCollection.length; i++) {
                dt = _dtCollection[i];
                if (dt.selector === dtSelector) {
                    return dt;
                }
            }
            return _setDataTable(dtSelector);
        },

        // Creates default config used to render data table.
        createConfig = function () {
            return {
                "bRetrieve" : true,                     /* Returns data-table */
                "bAutoWidth" : true,                    /* Automatically determine column widths */
                "bFilter" : true,                       /* Support table filtering */
                "bInfo" : true,                         /* Display results info */
                "bJQueryUI" : true,                     /* Use JqueryUI css theming */
                "bLengthChange" : true,                 /* Display items per page selector */
                "iDisplayLength" : 25,                  /* Number of records per page */
                "bPaginate" : true,                     /* Support pagination */
                "sPaginationType": "full_numbers",      /* Type of pagination */
                "bProcessing" : false,                  /* Display background processing dialog */
                "sDom" : '<"H"if>t<"F"lp>',             /* Dom related markup.   */
                "bSort" : true,                         /* Support sorting */
                "bSortClasses" : true,                  /* CSS classes for sort ??? */
                "bStateSave" : false,                   /* Save table state in cookie */
                "oLanguage" : {"sInfo" : "_START_ to _END_ of _TOTAL_ entries",
                                "sInfoEmpty" : "No records for display - please refine your search",
                                "sInfoFiltered" : "(filtered)",
                                "sLengthMenu": "_MENU_ per page",
                                "sSearch" : "Filter:",
                                "sZeroRecords" : "No records for display - please refine your filter"},  /* Various text to be displayed */
                 "fnFormatNumber" : function ( iIn ) {
                     if (iIn < 250) {
                         return iIn;
                     } else {
                         return iIn + "+";
                     }
                 }
            }
        },

        // Applies filters over a columns in the data table.
        applyFilter = function ( dtSelector, col ) {
            var
                dt = _getDataTable(dtSelector),
                f,
                v,
                i,
                filter = '^';
            if (dt !== undefined) {
                // Table level redraw.
                if (col === undefined) {
                    dt.grid.fnDraw();
                // Column level redraw.
                } else {
                    f = dt.colFilters.get(col);
                    if (f !== undefined) {
                        v = f.sourceValue();
                        if (v.length > 0 && parseInt(v) !== NaN) {
                            for (i = 0; i < v.length; i++) {
                                filter += '[' + v[i] + ']';
                            }
                            filter += '(?![0-9])$';
                        } else {
                            filter = v;
                        }
                        $jq(dtSelector).dataTable().fnFilter(
                                filter,
                                f.col,
                                true,
                                true
                        );
                        // Apply related column filters.
                        for (i = 0; i < f.related.length; i++) {
                            applyFilter(dt.selector, f.related[i]);
                        }
                    }
                }
            }
        },

        // Adds a range filter to the collection of managed filters.
        setRangeFilter = function ( dtSelector, col, colNull, minSelector, maxSelector, sourceSelector, sourceNull ) {
            var
                dt = _getDataTable(dtSelector);
            if (dt !== undefined) {
                // Wire up filter.
                dt.colFilters.set(col, [], sourceSelector, sourceNull);
                $jq(sourceSelector).change(
                    function () {applyFilter(dtSelector, undefined)}
                );

                // Register a data-tables range filter.
                $jq.fn.dataTableExt.afnFiltering.push(
                    function( oSettings, aData, iDataIndex ) {
                        var
                            min, max, value;

                        // Set value & range.
                        colNull = colNull === undefined ? "" : colNull;
                        value = aData[col] === colNull ? undefined : aData[col];
                        min = $jq(minSelector).val();
                        max = $jq(maxSelector).val();

                        // Assert value is in range.
                        if ( value == undefined ) {
                            return true;
                        }
                        else if ( min == "" && max == "" ) {
                            return true;
                        }
                        else if ( min == "" && value < max )
                        {
                            return true;
                        }
                        else if ( min < value && "" == max )
                        {
                            return true;
                        }
                        else if ( min < value && value < max )
                        {
                            return true;
                        }

                        // Value is out of range.
                        return false;
                    }
                );
            }
        },

        // Sets a column filter.
        setFilter = function ( dtSelector, col, colsRelated, sourceSelector, sourceNull ) {
            var
                dt = _getDataTable(dtSelector);
            if (dt !== undefined) {
                dt.colFilters.set(col, colsRelated, sourceSelector, sourceNull);
                $jq(sourceSelector).change(
                    function () {
                        applyFilter(dtSelector, col);
                    }
                );
            }
        },

        // Gets data array matching passed nodeset.
        getDataFromNodes = function ( dtSelector, nodeSet ) {
            var
                i,
                result = [],
                dt = _getDataTable(dtSelector);
            if (dt !== undefined && dt.grid !== undefined) {
                if ($jq.isArray(nodeSet) === false) {
                    result = dt.grid.fnGetData();
                } else {
                    for (i = 0; i < nodeSet.length; i++) {
                        result.push(dt.grid.fnGetData(nodeSet[i]));
                    }
                }
            }
            return result;
        },

        // Renders a data table.
        render = function ( dtSelector, dtConfig ) {
            var
                dt = _getDataTable(dtSelector);
            if (dt.config === undefined) {
                dt.config = dtConfig !== undefined ? dtConfig : createConfig();
            }
            dt.grid = $jq(dtSelector).dataTable(dt.config);
            return dt.grid;
        },

        // Deletes a row from table.
        deleteRow = function ( dtSelector, row ) {
            var
                dt = _getDataTable(dtSelector);
            if (dt !== undefined) {
                dt.grid.fnDeleteRow(row);
            }
        };

    // Register widget so that it is visible.
    $mf.registerWidget({
        id : 'grid',
        createConfigInfo : createConfig,
        render : render,
        applyFilter : applyFilter,
        setFilter : setFilter,
        setRangeFilter : setRangeFilter,
        getDataTable : function ( dtSelector ) {
            return _getDataTable(dtSelector).grid;
        },
        getDataTableWrapper : _getDataTable,
        getDataFromNodes : getDataFromNodes,
        deleteRow : deleteRow
    });
}());