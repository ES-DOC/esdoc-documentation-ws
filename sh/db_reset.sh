#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "API-DB : resetting ..."
	source $ESDOC_DIR_BASH/api/db_uninstall.sh
	source $ESDOC_DIR_BASH/api/db_install.sh
	log "API-DB : reset"
}

# Invoke entry point.
main
