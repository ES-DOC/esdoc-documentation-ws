#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	source $ESDOC_WS_HOME/sh/reset_logs.sh
	supervisord -c $ESDOC_WS_HOME/ops/config/supervisord.conf

	log "initialized web-service daemon"
}

# Invoke entry point.
main
