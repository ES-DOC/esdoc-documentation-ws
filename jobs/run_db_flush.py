# -*- coding: utf-8 -*-

"""
.. module:: run_db_flush.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Deletes (flushes) documents from database.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse


from esdoc_api import config
from esdoc_api.db import session
from esdoc_api.db.models import Document
from esdoc_api.db.models import DocumentDRS
from esdoc_api.db.models import DocumentExternalID
from esdoc_api.db.models import DocumentSummary
from esdoc_api.db.models import Project
from esdoc_api.db.dao import core as dao
from esdoc_api.utils import runtime as rt


# Define command line options.
_parser = argparse.ArgumentParser("Uningests documents from API database.")
_parser.add_argument(
    "--project",
    help="Projects whose documents will be uningested.",
    dest="project",
    type=str
    )
_parser.add_argument(
    "--source",
    help="Source whose documents will be uningested.",
    dest="source",
    type=str,
    default=None
    )


def _execute(project_code, source):
    """Executes document deletion.

    """
    # Format input params.
    project_code = unicode(project_code).strip().lower()
    if source is not None:
        source = unicode(source).strip().lower()
        if len(source) == 0:
            source = None

    # Map project code to project entry in db.
    project = dao.get_by_name(Project, project_code)
    if project is None:
        rt.log("Project code [{}] is unsupported".format(project_code))
        return

    # Build queries.
    qry1 = session.query(Document.ID)
    qry1 = qry1.filter(Document.Project_ID == project.ID)
    if source is not None:
        qry1 = qry1.filter(Document.Source_Key == source)

    qry2 = session.query(DocumentDRS)
    qry2 = qry2.filter(DocumentDRS.Document_ID.in_(qry1.subquery()))

    qry3 = session.query(DocumentExternalID)
    qry3 = qry3.filter(DocumentExternalID.Document_ID.in_(qry1.subquery()))

    qry4 = session.query(DocumentSummary)
    qry4 = qry4.filter(DocumentSummary.Document_ID.in_(qry1.subquery()))

    # Delete data.
    qry4.delete(synchronize_session=False)
    qry3.delete(synchronize_session=False)
    qry2.delete(synchronize_session=False)
    qry1.delete()


def _main(project_code, source):
    """Main entry point.

    """
    if source == "*" or len(source) == 0:
    	source = None

    session.start(config.db)
    try:
        _execute(project_code, source)
    except Exception as err:
    	print err
        session.rollback()
        rt.log_db_error(err)
    else:
        session.commit()
    finally:
        session.end()


# Main entry point.
if __name__ == '__main__':
    args = _parser.parse_args()
    _main(args.project, args.source)

