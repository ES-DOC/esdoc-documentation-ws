"""
.. module:: initialize_ingest_state.py
   :platform: Unix
   :synopsis: Initializes collection of supported ingest states.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from .. import (
    models, 
    session
    )



def execute():
    """Initializes collection of supported ingest states.

    """
    # QUEUED.
    i = models.IngestState()
    i.Name = models.INGEST_STATE_QUEUED
    i.Description = "Ingest has been setup and is awaiting execution."
    i.Code = 100
    session.insert(i)

    # RUNNING.
    i = models.IngestState()
    i.Name = models.INGEST_STATE_RUNNING
    i.Description = "Ingest is being executed."
    i.Code = 200
    session.insert(i)

    # SUSPENDED.
    i = models.IngestState()
    i.Name = models.INGEST_STATE_SUSPENDED
    i.Description = "Ingest has been suspended."
    i.Code = 300
    session.insert(i)

    # COMPLETE.
    i = models.IngestState()
    i.Name = models.INGEST_STATE_COMPLETE
    i.Description = "Ingest has completed with success."
    i.Code = 400
    session.insert(i)

    # COMPLETE_ERROR.
    i = models.IngestState()
    i.Name = models.INGEST_STATE_ERROR
    i.Description = "Ingest error occurred."
    i.Code = 999
    session.insert(i)
