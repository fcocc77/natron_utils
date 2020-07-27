# api: este archivo permite subministrar un proyecto videovina,
# que se envio desde el editor web de videovina.
from nx import createNode
import json
import os
import shutil
from sys import argv
from util import fread, jread


vinarender_path = fread('/etc/vinarender')
env = jread(vinarender_path + '/etc/videovina.json')

# datos de vinarender
data = json.loads(argv[2].replace("'", '"'))

user = data['user']
project_name = data['project_name']
project_type = data['project_type']

# directorio local para el usuario y proyecto
project_dir = env.local + '/' + user + "/" + project_name
if not os.path.isdir(project_dir):
    os.makedirs(project_dir)


videovina_project_dir = env.s3 + '/private/' + user + '/projects/' + project_name
videovina_project = videovina_project_dir + '/project.json'
base_projects_dir = env.assets + '/templates_base/' + project_type + '/comp/ntp'  # Remplazar 'templates_base' solo por 'templates'

multi_project_dir = project_dir + '/comp'
if not os.path.isdir(multi_project_dir):
    os.makedirs(multi_project_dir)


# Copia footage, project.json de amazon S3 y lo copia en el directorio compartido local
project_json = project_dir + '/project.json'
shutil.copytree(videovina_project_dir + '/footage', project_dir + '/footage')
shutil.copy(videovina_project, project_json)


# creacion de nodo videovina y ntprender
vinarender_node = createNode('videovina')
ntprender = createNode('ntprender')
ntprender.connectInput(0, vinarender_node)

# actualiza los datos del proyecto de videovina al nodo videovina
vinarender_node.getParam('videovina_project').set(project_json)
vinarender_node.getParam('update_videovina_project').trigger()

# envia a crear los proyectos a vinarender
ntprender.getParam('output_folder').set(base_projects_dir)
ntprender.getParam('output_production_folder').set(multi_project_dir)
ntprender.getParam('job_name').set('multi_project: ' + user + ':' + project_name)
ntprender.getParam('send_as_production').trigger()


# chmod temporal
os.system('chmod 777 -R ' + env.local)
