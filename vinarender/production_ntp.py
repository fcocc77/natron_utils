from sys import argv
import NatronEngine
import os
import json
from util import fread, fwrite
from time import sleep

from vina import get_videovina
from develop import update_post_fx
from slides import clamp_slides
import nx

# datos de vinarender
data = json.loads(argv[3].replace("'", '"'))
project = data['project']
last_project = data['last_project']
last_slide = data['last_slide']
# ----------------------

_app = app1.loadProject(project)
nx._app = _app

if last_project:
    clamp_slides(0, last_slide)
    update_post_fx()

get_videovina().getParam('update_videovina_project').trigger()
nx.saveProject()

print 'Testing Error: 0'
