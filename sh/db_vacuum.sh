#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "DB : vacuuming postgres db ..."

	psql -U esdoc_db_admin -d esdoc_api -q -f $ESDOC_WS_HOME/sh/db_vacuum.sql

	log "DB : vacuumed postgres db"
}

# Invoke entry point.
main
