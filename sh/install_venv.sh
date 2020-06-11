#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "installing virtual environment ..."

    pyenv local 2.7.17
    pip install --upgrade pip
    pip install --upgrade pipenv
    pushd $ESDOC_WS_HOME
    pipenv install -r $ESDOC_WS_HOME/requirements.txt    
}

# Invoke entry point.
main
