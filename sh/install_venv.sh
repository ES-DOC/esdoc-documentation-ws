#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "installing virtual environment ..."

    pip2 install --upgrade pip
    pip2 install --upgrade virtualenv
    virtualenv $ESDOC_WS_HOME/ops/venv
    source $ESDOC_WS_HOME/sh/activate_venv.sh
    pip2 install --upgrade pip
    pip2 install --upgrade --no-cache-dir -I -r $ESDOC_WS_HOME/resources/requirements.txt
    pip2 install --upgrade --no-cache-dir -I -r $ESDOC_WS_HOME/resources/requirements-pyesdoc.txt
    deactivate
}

# Invoke entry point.
main
