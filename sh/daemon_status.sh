#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	pushd $ESDOC_WS_HOME
	supervisorctl -c $ESDOC_WS_HOME/ops/config/supervisord.conf status all
	popd
}

# Invoke entry point.
main
