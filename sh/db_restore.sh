#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "DB : restoring ..."

    source $ESDOC_WS_HOME/sh/db_uninstall.sh
    source $ESDOC_WS_HOME/sh/db_install.sh
    psql -U esdoc_api_db_admin esdoc_api -f $ESDOC_WS_HOME/resources/db -q

	log "DB : restored"
}

# Invoke entry point.
main
