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
from pictures import generate_pictures

# datos de vinarender
data = json.loads(argv[3].replace("'", '"'))
base_project = data['project']
original_slides_range = data['range']
slides_range = data['slides']
output_folder = data['output_folder']
# ----------------------

base_project_name = os.path.basename(base_project)[:-4]

if not os.path.isdir(output_folder):
    os.makedirs(output_folder)
    os.system('chmod 777 -R ' + output_folder)

project_name = base_project_name + '_' + \
    str(original_slides_range[0]) + '-' + str(original_slides_range[1])

project = output_folder + '/' + project_name + '.ntp'

_app = app1.loadProject(base_project)

nx._app = _app

generate_production_slides(None, _app, _app, slides_range, force=True)
get_videovina().getParam('generate_pictures').trigger()

_app.saveProjectAs(project)

testing(
    app=_app,
    project=project,
    slide_range=slides_range
)
