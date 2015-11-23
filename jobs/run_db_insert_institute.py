# -*- coding: utf-8 -*-
from tornado.options import define, options

from esdoc_api import db, config



# Setup command line options.
define("name", help="Institute name", type=unicode)


def _main():
    """Main entry point.

    """
    # Start session.
    db.session.start(config.db)

    # Insert into db.
    instance = db.dao.create_institute(options.name)
    db.session.insert(instance)

    # End session.
    db.session.end()



# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
