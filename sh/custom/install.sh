#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	cp $ESDOC_WS_HOME/resources/template-pyesdoc.conf $ESDOC_WS_HOME/ops/config/pyesdoc.conf
	log "custom configuration files initialized"

	git clone https://github.com/ES-DOC/esdoc-archive.git $ESDOC_WS_HOME/ops/libs/esdoc-archive
	git clone https://github.com/ES-DOC/esdoc-py-client.git $ESDOC_WS_HOME/ops/libs/esdoc-py-client
	log "custom libraries initialized"
}

# Invoke entry point.
main
