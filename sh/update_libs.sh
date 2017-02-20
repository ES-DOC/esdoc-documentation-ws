#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    cd $ESDOC_WS_HOME/ops/libs/esdoc-py-client
    git pull

    cd $ESDOC_WS_HOME/ops/libs/esdoc-archive
    git pull
}

# Invoke entry point.
main
