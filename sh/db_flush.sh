#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/bash/init.sh

# Main entry point.
main()
{
    log "DB: flushing $1 documents from api database ..."

	activate_venv api
	python $ESDOC_WS_HOME/sh/db_flush.py --project=$1 --source=$2

    log "DB: flushed $1 documents from api database"
}

# Invoke entry point.
main $1 $2