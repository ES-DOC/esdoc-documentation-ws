printf "*-----------------------------------*\n"

# ---------------------------------------------------------
# STEP 1 : Run ingest.
# ---------------------------------------------------------
printf "Ingesting ..."

# Setup.
source /Users/markmorgan/Development/python_venv/mf/bin/activate
python2.6 /Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/deploy/db_ingest.py

printf "*-----------------------------------*\n"

# Display notice.
printf "*************************************\n"
printf "pylons cim db ingest :: COMPLETE\n"
printf "*************************************\n"

exit 0