#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    pushd $ESDOC_WS_HOME
	git pull
}

# Invoke entry point.
main
