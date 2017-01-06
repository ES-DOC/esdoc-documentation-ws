#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	activate_venv
    pip install --upgrade pip
    pip install --upgrade --no-cache-dir -I -r $ESDOC_WS_HOME/requirements.txt
    deactivate

    log "SH : virtual environment updated"
}

# Invoke entry point.
main
