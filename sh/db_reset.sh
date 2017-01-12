#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "DB : resetting ..."
	source $ESDOC_WS_HOME/sh/db_uninstall.sh
	source $ESDOC_WS_HOME/sh/db_install.sh
	log "DB : reset"
}

# Invoke entry point.
main
