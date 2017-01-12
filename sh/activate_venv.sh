#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_WS_HOME
	export PYTHONPATH=$PYTHONPATH:$PYESDOC_HOME
	source $ESDOC_WS_HOME/ops/venv/bin/activate
}

# Invoke entry point.
main
