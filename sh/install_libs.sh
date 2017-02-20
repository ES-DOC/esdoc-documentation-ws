#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	git clone https://github.com/ES-DOC/esdoc-archive.git $ESDOC_WS_HOME/ops/libs/esdoc-archive
	log "archive installed @ "$ESDOC_WS_HOME/ops/libs/esdoc-archive
	git clone https://github.com/ES-DOC/esdoc-py-client.git $ESDOC_WS_HOME/ops/libs/esdoc-py-client
	log "pyesdoc installed @ "$ESDOC_WS_HOME/ops/libs/esdoc-py-client
}

# Invoke entry point.
main
