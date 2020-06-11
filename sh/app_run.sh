#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "running ..."

    pushd $ESDOC_WS_HOME
	pipenv run python $ESDOC_WS_HOME/sh/app_run.py
}

# Invoke entry point.
main
