#!/bin/bash

# Wraps standard echo by adding application prefix.
log()
{
	declare now=`date +%Y-%m-%dT%H:%M:%S`
	declare tabs=''
	if [ "$1" ]; then
		if [ "$2" ]; then
			for ((i=0; i<$2; i++))
			do
				declare tabs+='\t'
			done
	    	echo -e $now" [INFO] :: ESDOC_WS > "$tabs$1
	    else
	    	echo -e $now" [INFO] :: ESDOC_WS > "$1
	    fi
	else
	    echo -e $now" [INFO] :: ESDOC_WS > "
	fi
}

activate_venv()
{
	source $ESDOC_WS_HOME/venv/bin/activate
}
