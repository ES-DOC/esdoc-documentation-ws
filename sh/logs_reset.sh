#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	rm $ESDOC_WS_HOME/ops/logs/*.log

	log "logs reset"
}

# Invoke entry point.
main
