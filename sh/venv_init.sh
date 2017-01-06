#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "SH : installing virtual environment ..."

    pip install --upgrade pip
    pip install --upgrade virtualenv
    virtualenv $ESDOC_WS_HOME/venv
    activate_venv
    pip install --upgrade pip
    pip install --upgrade --no-cache-dir -I -r $ESDOC_WS_HOME/requirements.txt
    deactivate
}

# Invoke entry point.
main
