#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	source $ESDOC_WS_HOME/sh/daemon_stop.sh
	source $ESDOC_WS_HOME/sh/daemon_start.sh
}

# Invoke entry point.
main
