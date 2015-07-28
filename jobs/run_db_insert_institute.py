# -*- coding: utf-8 -*-
from tornado.options import define, options

from esdoc_api import db, config



# Setup command line options.
define("name", help="Institute name", type=unicode)
define("description", help="Institute long name", type=unicode)
define("country", help="Institute country code", type=unicode)
define("homepage", help="Institute home page", type=unicode)


def _main():
    """Main entry point.

    """
    print options.name, options.description, options.country, options.homepage
    # Start session.
    db.session.start(config.db)

    # Insert into db.
    instance = db.dao.create_institute(
        "NOAA", "National Oceanic and Atmosphere Administration", "US", "http://www.noaa.gov/")
    # instance = db.dao.create_institute(
    #     options.name, options.description, options.country, options.homepage)
    db.session.insert(instance)

    # End session.
    db.session.end()



# Main entry point.
if __name__ == '__main__':
    options.parse_command_line()
    _main()
