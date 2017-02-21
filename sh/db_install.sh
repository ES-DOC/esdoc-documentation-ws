#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Create db users.
_db_create_users()
{
	log "DB : creating database users"
	createuser -U postgres -d -s esdoc_db_admin
	createuser -U esdoc_db_admin -D -S -R esdoc_db_user
}

# Create db.
_db_create()
{
	log "DB : creating database"
	createdb -U esdoc_db_admin -e -O esdoc_db_admin -T template0 esdoc_api
}

# Grant db permissions.
_db_grant_permissions()
{
	log "DB : granting database permissions"
	psql -U esdoc_db_admin -d esdoc_api -a -f $ESDOC_WS_HOME/db_permissions.sql
}

# Setup db.
_db_setup()
{
	log "DB : setting up database"

    source $ESDOC_WS_HOME/sh/db_setup.sh
}

# Main entry point.
main()
{
	log "DB : installing ..."

	_db_create_users
	_db_create
	_db_setup
	_db_grant_permissions

	log "DB : installed"
}

# Invoke entry point.
main
