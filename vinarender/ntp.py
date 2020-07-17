from sys import argv
import NatronEngine
import os
import json
from util import fread, fwrite
from time import sleep

from slides import get_slides
from production import generate_production_slides
from vina import get_videovina
from project import testing
import nx

# datos de vinarender
data = json.loads(argv[3].replace("'", '"'))
base_project = data['project']
frame_range = data['frames']
slides_range = data['slides']
output_folder = data['output_folder']
# ----------------------

base_project_name = os.path.basename(base_project)[:-4]

if not os.path.isdir(output_folder):
    os.makedirs(output_folder)
    os.system('chmod 777 -R ' + output_folder)

project_name = base_project_name + '_' + \
    str(frame_range[0]) + '-' + str(frame_range[1])

project = output_folder + '/' + project_name + '.ntp'

_app = app1.loadProject(base_project)

nx._app = _app

generate_production_slides(None, _app, _app, slides_range, force=True)

_app.saveProjectAs(project)

testing(
    app=_app,
    project=project,
    slide_range=slides_range,
    format=2,  # quarter, half, hd, 4k
    speed=0  # Slow, Normal, Fast
)
