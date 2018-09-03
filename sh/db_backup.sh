#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "DB : backing up ..."

	pg_dump esdoc_api -U esdoc_api_db_admin -c -f $ESDOC_WS_HOME/resources/db;

	log "DB : backed up @ "$ESDOC_WS_HOME/resources/db
}

# Invoke entry point.
main
