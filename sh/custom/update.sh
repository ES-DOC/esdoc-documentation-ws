#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	cp $ESDOC_WS_HOME/resources/template-pyesdoc.conf $ESDOC_WS_HOME/ops/config/pyesdoc.conf
	log "custom configuration files updated"
    cd $ESDOC_WS_HOME/ops/libs/esdoc-py-client
    git pull
    cd $ESDOC_WS_HOME/ops/libs/esdoc-archive
    git pull
    cd $ESDOC_WS_HOME
}

# Invoke entry point.
main
