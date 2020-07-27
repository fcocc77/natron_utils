from sys import argv
import NatronEngine
import os
import json
from util import fread, fwrite
from time import sleep
from project import testing

from vina import get_videovina
from develop import update_post_fx
from slides import clamp_slides
import nx
from util import jread, fread

# datos de vinarender
data = json.loads(argv[3].replace("'", '"'))
project = data['project']
last_project = data['last_project']
last_slide = data['last_slide']
speed = data['speed']
format = data['format']
user = data['user']
project_name = data['project_name']
# ----------------------

_app = app1.loadProject(project)
nx._app = _app

if last_project:
    clamp_slides(0, last_slide)
    update_post_fx()


vinarender_path = fread('/etc/vinarender')
env = jread(vinarender_path + '/etc/videovina.json')

project_json = env.local + '/' + user + "/" + project_name + '/project.json'

videovina_node = get_videovina()
videovina_node.getParam('videovina_project').set(project_json)
videovina_node.getParam('update_videovina_project').trigger()

nx.saveProject()
os.system('chmod 777 "' + project + '"')

testing(
    app=_app,
    project=project,
    # slide_range=slides_range,
    speed=speed,
    format=format
)
