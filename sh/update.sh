#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

_update_src()
{
    pushd $ESDOC_WS_HOME
	git pull
}

_update_venv()
{
    pushd $ESDOC_WS_HOME
    pipenv install -r $ESDOC_WS_HOME/requirements.txt
}

# Main entry point.
main()
{
    log "update starts ..."

    _update_src
    _update_venv

    log "update complete"
}

# Invoke entry point.
main
