#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	cp $ESDOC_WS_HOME/templates/template-pyesdoc.conf $ESDOC_WS_HOME/ops/config/pyesdoc.conf
	cp $ESDOC_WS_HOME/templates/template-supervisord.conf $ESDOC_WS_HOME/ops/config/supervisord.conf
	cp $ESDOC_WS_HOME/templates/template-ws.conf $ESDOC_WS_HOME/ops/config/ws.conf

	log "configuration files updated"
}

# Invoke entry point.
main
