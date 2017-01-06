#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "TESTS : running ..."

    activate_venv
    nosetests -v -s $ESDOC_WS_HOME/tests

    log "TESTS : complete ..."
}

# Invoke entry point.
main
