"""
.. module:: esdoc_api.lib.repo.init.populate_ingest_state.py
   :platform: Unix
   :synopsis: Populates collection of supported ingest states.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# -*- coding: iso-8859-15 -*-

# Module imports.
import esdoc_api.lib.repo.models as models
import esdoc_api.lib.repo.session as session



def populate_ingest_state():
    """Populates collection of supported ingest states.

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
