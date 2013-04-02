#!/bin/bash
# ---------------------------------------------------------
# Installs esdoc_api virtual environment.
# ---------------------------------------------------------

# Display notice.
printf "*************************************\n"
printf "pylons venv install :: STARTS\n"
printf "*************************************\n"

# Set paths.
HOME=/home/esdoc
VENV=$HOME/venv/api

# Initialize virtual environment:
# ... create
curl -o $VENV/virtualenv.py  https://bitbucket.org/ianb/virtualenv/raw/8dd7663d9811/virtualenv.py
python2.6 $VENV/virtualenv.py $VENV
# ... activate
source $VENV/bin/activate
# ... extend
pip install Pylons==1.0
pip install Sqlalchemy
pip install elixir
pip install lxml
pip install feedparser
pip install httplib2
pip install python_dateutil
pip uninstall webob
pip install webob==1.0.8

# Display notice.
printf "*************************************\n"
printf "pylons venv install :: COMPLETE\n"
printf "*************************************\n"

exit 0


