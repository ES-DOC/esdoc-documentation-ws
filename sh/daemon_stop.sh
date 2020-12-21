#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	pushd $ESDOC_WS_HOME
	supervisorctl -c $ESDOC_WS_HOME/ops/config/supervisord.conf stop all
	supervisorctl -c $ESDOC_WS_HOME/ops/config/supervisord.conf shutdown
	popd

	log "killed web-service daemon"
}

# Invoke entry point.
main
