#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	supervisorctl -c $ESDOC_WS_HOME/ops/config/supervisord.conf stop all
	supervisorctl -c $ESDOC_WS_HOME/ops/config/supervisord.conf shutdown

	log "WEB : killed web-service daemon"
}

# Invoke entry point.
main
