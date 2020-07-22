from sys import argv
import NatronEngine
import os
import json
from util import fread, fwrite
from time import sleep

from vina import get_videovina
import nx

# datos de vinarender
data = json.loads(argv[3].replace("'", '"'))
project = data['project']
output_folder = data['output_folder']
# ----------------------

_app = app1.loadProject(project)
nx._app = _app


get_videovina().getParam('update_videovina_project').trigger()
nx.saveProject()


print 'Testing Error: 0'
