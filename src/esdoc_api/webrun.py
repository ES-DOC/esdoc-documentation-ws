"""
Primary web server entry point.
"""

# Module imports.
import os
import os.path


from paste.script.serve import ServeCommand


if __name__ == "__main__":
    print "ES-DOC API - web server starting.";


def _get_user_name():
    """Returns current user name.
    
    """
    username = None
    try:
        import pwd
        username = pwd.getpwuid(os.getuid()).pw_name
    except ImportError:
        username = os.environ.get("USERNAME")
    print "ENVIRONMENT :: USER :: {0}.".format(username)
    return username


def get_ini_file_path():
    """Returns the ini file to be used.
    
    """
    user = _get_user_name()
    path = u"config/ini_files/{0}.ini".format(user)
    if os.path.exists(path) == False:
        path = u"config/ini_files/config.ini"
    return os.path.abspath(path)


ini_file = get_ini_file_path()
ServeCommand("serve").run([ini_file])
