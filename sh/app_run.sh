#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "running ..."

    activate_venv
	python $ESDOC_WS_HOME/sh/app_run.py
}

# Invoke entry point.
main
