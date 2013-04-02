printf "*-----------------------------------*\n"

# ---------------------------------------------------------
# STEP 1 : Run db setup.
# ---------------------------------------------------------
printf "Setting up ..."

# Setup.
source /Users/markmorgan/Development/python_venv/mf/bin/activate
python2.6 /Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/deploy/db_setup.py

printf "*-----------------------------------*\n"

# Display notice.
printf "*************************************\n"
printf "pylons cim db setup :: COMPLETE\n"
printf "*************************************\n"

exit 0