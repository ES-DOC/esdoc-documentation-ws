"""Populates collection of supported ingest states.

"""
# -*- coding: iso-8859-15 -*-

# Module imports.
from esdoc_api.models.entities.ingest_state import *

# Module exports.
__all__ = ['populate_ingest_state']


def populate_ingest_state():
    """Populates collection of supported ingest states.

    Keyword Arguments:
    session - db sesssion.
    """
    # QUEUED.
    ss = IngestState()
    ss.Name = EXECUTION_STATE_QUEUED
    ss.Description = "Ingest has been setup and is awaiting execution."
    ss.Code = 100

    # RUNNING.
    ss = IngestState()
    ss.Name = EXECUTION_STATE_RUNNING
    ss.Description = "Ingest is being executed."
    ss.Code = 200

    # SUSPENDED.
    ss = IngestState()
    ss.Name = EXECUTION_STATE_SUSPENDED
    ss.Description = "Ingest has been suspended."
    ss.Code = 300

    # COMPLETE.
    ss = IngestState()
    ss.Name = EXECUTION_STATE_COMPLETE
    ss.Description = "Ingest has completed with success."
    ss.Code = 400

    # COMPLETE_ERROR.
    ss = IngestState()
    ss.Name = EXECUTION_STATE_ERROR
    ss.Description = "Ingest error occurred."
    ss.Code = 999
