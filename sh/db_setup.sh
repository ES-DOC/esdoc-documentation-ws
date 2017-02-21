#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "DB : setting up ..."

    source $ESDOC_WS_HOME/sh/activate_venv.sh
    python $ESDOC_WS_HOME/sh/db_setup.py

	log "DB : set up"
}

# Invoke entry point.
main
