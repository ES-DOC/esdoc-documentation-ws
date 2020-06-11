#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	log "DB : setting up ..."

    pushd $ESDOC_WS_HOME
    pipenv run python $ESDOC_WS_HOME/sh/db_setup.py

	log "DB : set up"
}

# Invoke entry point.
main
