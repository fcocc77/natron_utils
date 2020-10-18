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
original_slides_range = data['slide']['range']
slides_range = data['slide']['slides']
output_folder = data['output_folder']
src_path = data['src_path']
dst_path = data['dst_path']
#
#

# correccion de rutas
base_project = base_project.replace(src_path, dst_path)
output_folder = output_folder.replace(src_path, dst_path)
#
#


base_project_name = os.path.basename(base_project)[:-4]

if not os.path.isdir(output_folder):
    os.makedirs(output_folder)
    os.system('chmod 777 -R ' + output_folder)

project_name = base_project_name + '_' + str(original_slides_range[0]) + '-' + str(original_slides_range[1])

project = output_folder + '/' + project_name + '.ntp'

_app = app1.loadProject(base_project)

nx._app = _app

generate_production_slides(None, _app, _app, slides_range, force=True)
videovina_node = get_videovina()
videovina_node.getParam('reformat').set(False)
videovina_node.getParam('generate_pictures').trigger()

_app.saveProjectAs(project)
os.system('chmod 777 "' + project + '"')

testing(
    app=_app,
    project=project,
    slide_range=slides_range
)
