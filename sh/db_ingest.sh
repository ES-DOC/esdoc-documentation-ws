#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "API-DB: ingesting from pyesdoc archive ..."

    activate_venv api
    python $ESDOC_HOME/bash/api/db_ingest.py

    log "API-DB: ingested from pyesdoc archive"
}

# Invoke entry point.
main
