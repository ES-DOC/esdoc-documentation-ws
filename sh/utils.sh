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
	    	echo -e $now" [INFO] :: ESDOC-WS > "$tabs$1
	    else
	    	echo -e $now" [INFO] :: ESDOC-WS > "$1
	    fi
	else
	    echo -e $now" [INFO] :: ESDOC-WS > "
	fi
}

activate_venv()
{
	export PYTHONPATH=$PYTHONPATH:$ESDOC_WS_HOME
	export PYTHONPATH=$PYTHONPATH:$ESDOC_WS_HOME/ops/esdoc-py-client
	source $ESDOC_WS_HOME/ops/venv/bin/activate
}
