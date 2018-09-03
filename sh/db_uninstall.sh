#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Create db users.
_db_drop_users()
{
	log "DB : deleting database users"

	dropuser -U esdoc_api_db_admin esdoc_api_db_user
	dropuser -U $ESDOC_API_DB_SYSTEM_USER esdoc_api_db_admin
}

# Drop db.
_db_drop()
{
	log "DB : dropping database"

	dropdb -U esdoc_api_db_admin esdoc_api
}

# Main entry point.
main()
{
	log "DB : uninstalling ..."
	_db_drop
	_db_drop_users
	log "DB : uninstalled"
}

# Invoke entry point.
main
