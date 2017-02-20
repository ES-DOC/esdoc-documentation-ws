#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	cp $ESDOC_WS_HOME/resources/template-supervisord.conf $ESDOC_WS_HOME/ops/config/supervisord.conf
	cp $ESDOC_WS_HOME/resources/template-ws.conf $ESDOC_WS_HOME/ops/config/ws.conf
	cp $ESDOC_WS_HOME/resources/template-pyesdoc.conf $ESDOC_WS_HOME/ops/config/pyesdoc.conf

	log "configuration files initialized"
}

# Invoke entry point.
main
