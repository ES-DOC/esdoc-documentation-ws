# -*- coding: utf-8 -*-
from esdoc_api.db.ingest.execute import (
	process_archived as execute,
	process_doc as ingest_doc
	)
from esdoc_api.db.ingest.undo import execute as undo
