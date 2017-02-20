#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "DB: ingesting from pyesdoc archive ..."

    source $ESDOC_WS_HOME/sh/activate_venv.sh
    python $ESDOC_WS_HOME/sh/custom/db_ingest.py

    log "DB: ingested from pyesdoc archive"
}

# Invoke entry point.
main
