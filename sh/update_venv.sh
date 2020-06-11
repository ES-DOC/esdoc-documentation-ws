#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    pushd $ESDOC_WS_HOME
    pipenv install -r $ESDOC_WS_HOME/requirements.txt
}

# Invoke entry point.
main
