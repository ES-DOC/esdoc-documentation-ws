#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "update starts ..."

	source $ESDOC_WS_HOME/sh/update_src.sh
	source $ESDOC_WS_HOME/sh/update_venv.sh

    log "update complete"
}

# Invoke entry point.
main
