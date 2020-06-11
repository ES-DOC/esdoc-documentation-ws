#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "DB: ingesting from pyesdoc archive ..."

    pushd $ESDOC_WS_HOME
    pipenv run python $ESDOC_WS_HOME/sh/db_ingest.py

    log "DB: ingested from pyesdoc archive"
}

# Invoke entry point.
main
