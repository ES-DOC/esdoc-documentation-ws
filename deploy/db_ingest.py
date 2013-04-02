import sys

# Extend python path.
sys.path.append('/Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/src')
sys.path.append('/Users/markmorgan/Development/sourcetree/esdoc/esdoc-api/src/esdoc_api')

# Ingest.
from esdoc_api.lib.db.ingestion.do_ingest import execute_ingestion
execute_ingestion()