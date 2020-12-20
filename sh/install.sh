#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

install_config()
{
	cp $ESDOC_WS_HOME/resources/template-supervisord.conf $ESDOC_WS_HOME/ops/config/supervisord.conf
	cp $ESDOC_WS_HOME/resources/template-ws.conf $ESDOC_WS_HOME/ops/config/ws.conf
	cp $ESDOC_WS_HOME/resources/template-pyesdoc.conf $HOME/.pyesdoc

	log "configuration files initialized"
}

install_venv()
{
    log "installing virtual environment ..."

	pushd $ESDOC_WS_HOME

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

    install_config
    install_venv

    log "install complete"
}

# Invoke entry point.
main
