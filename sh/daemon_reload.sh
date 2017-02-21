#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	source $ESDOC_WS_HOME/sh/daemon_stop.sh
	source $ESDOC_WS_HOME/sh/daemon_start.sh
	sleep 3.0
	source $ESDOC_WS_HOME/sh/daemon_status.sh
}

# Invoke entry point.
main
