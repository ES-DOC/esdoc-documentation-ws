#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "DB : truncating ..."

    source $ESDOC_WS_HOME/sh/activate_venv.sh
	psql -U $1 -d esdoc_api -a -f $ESDOC_WS_HOME/db_truncate.sql

	log "DB : truncated"
}

# Invoke entry point.
main $1
