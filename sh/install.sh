#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

install_config()
{
	cp $ESDOC_WS_HOME/resources/template-supervisord.conf $ESDOC_WS_HOME/ops/config/supervisord.conf
	cp $ESDOC_WS_HOME/resources/template-ws.conf $ESDOC_WS_HOME/ops/config/ws.conf
	cp $ESDOC_WS_HOME/resources/template-pyesdoc.conf $ESDOC_WS_HOME/ops/config/pyesdoc.conf

	log "configuration files initialized"
}

_install_venv()
{
    log "installing virtual environment ..."

    # Update pip / pipenv to latest versions.
    pip install --upgrade pip
    pip install --upgrade pipenv

	# Install venv using pipenv.
    pushd $ESDOC_WS_HOME
    pipenv install -r $ESDOC_WS_HOME/requirements.txt    
}

# Main entry point.
main()
{
    log "install starts ..."

    _install_config
    _install_venv

    log "install complete"
}

# Invoke entry point.
main
