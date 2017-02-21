#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	source $ESDOC_WS_HOME/sh/activate_venv.sh
    $ESDOC_WS_PIP install --upgrade pip
    $ESDOC_WS_PIP install --upgrade --no-cache-dir -I -r $ESDOC_WS_HOME/resources/requirements.txt
    $ESDOC_WS_PIP install --upgrade --no-cache-dir -I -r $ESDOC_WS_HOME/resources/requirements-pyesdoc.txt
    deactivate
}

# Invoke entry point.
main
