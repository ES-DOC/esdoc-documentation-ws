#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "update starts ..."

    pushd $ESDOC_WS_HOME
    git pull
    pipenv install -r $ESDOC_WS_HOME/requirements.txt
    popd

    log "update complete"
}

# Invoke entry point.
main
