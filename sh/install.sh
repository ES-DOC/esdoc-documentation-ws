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
	pushd $ESDOC_WS_HOME

    log "installing virtual environment ..."

    # Update pip / pipenv to latest versions.
    pip install --upgrade pip
    pip install --upgrade pipenv

	# Install venv using pipenv.
    pipenv install -r $ESDOC_WS_HOME/requirements.txt    

    popd
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
