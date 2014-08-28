import sys
import site
import os

prev_sys_path = list(sys.path)

# add the site-packages of our virtualenv as a site dir
vepath = '/home/esdoc/webapps/test_api1/venv/lib/python2.6/site-packages'
site.addsitedir(vepath)

# add the app's directory to the PYTHONPATH
sys.path.append('/home/esdoc/webapps/test_api1/app/src')
sys.path.append('/home/esdoc/webapps/test_api1/app/src/esdoc_api')

# reorder sys.path so new directories from the addsitedir show up first
new_sys_path = [p for p in sys.path if p not in prev_sys_path]
for item in new_sys_path:
    sys.path.remove(item)
sys.path[:0] = new_sys_path

from paste.deploy import loadapp
application = loadapp('config:/home/esdoc/webapps/test_api1/app/prod.ini')

