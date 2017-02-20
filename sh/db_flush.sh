#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "DB: flushing $1 documents from api database ..."

	source $ESDOC_WS_HOME/sh/activate_venv.sh
	python $ESDOC_WS_HOME/sh/custom/db_flush.py --project=$1 --source=$2

    log "DB: flushed $1 documents from api database"
}

# Invoke entry point.
main $1 $2