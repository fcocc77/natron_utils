# api: este archivo permite subministrar un proyecto videovina,
# que se envio desde el editor web de videovina.
from nx import createNode
from vina import get_videovina
import json
import os
import shutil
from sys import argv
from util import fread, jread, makedirs


vinarender_path = fread('/etc/vinarender')
env = jread(vinarender_path + '/etc/videovina.json')

# datos de vinarender
data = json.loads(argv[2].replace("'", '"'))
user = data['user']
project_name = data['project_name']
action = data['action']


# directorio local para el usuario y proyecto
project_dir = env.local + '/' + user + "/" + project_name
makedirs(project_dir)

multi_project_dir = project_dir + '/comp'
makedirs(multi_project_dir)


submit_ntp = project_dir + '/submit.ntp'


def create_multi_project():
    project_type = data['project_type']

    videovina_project_dir = env.s3 + '/private/' + user + '/projects/' + project_name
    videovina_project = videovina_project_dir + '/project.json'
    base_projects_dir = env.assets + '/templates_base/' + project_type + '/comp/ntp'  # Remplazar 'templates_base' solo por 'templates'

    # Copia footage, project.json de amazon S3 y lo copia en el directorio compartido local
    project_json = project_dir + '/project.json'
    shutil.copy(videovina_project, project_json)

    s3_footage = videovina_project_dir + '/footage'
    loal_footage = project_dir + '/footage'
    makedirs(loal_footage)
    # copia las fotos de a una, por si ya estan en el directorio local
    # asi no se gasta tanto trafico
    for photo in os.listdir(s3_footage):
        src = s3_footage + '/' + photo
        dst = loal_footage + '/' + photo
        if not os.path.isfile(dst):
            shutil.copy(src, dst)

    # creacion de nodo videovina y ntprender
    videovina_node = createNode('videovina')
    ntprender = createNode('ntprender')
    ntprender.connectInput(0, videovina_node)

    # actualiza los datos del proyecto de videovina al nodo videovina
    videovina_node.getParam('videovina_project').set(project_json)
    videovina_node.getParam('update_videovina_project').trigger()

    # envia a crear los proyectos a vinarender
    ntprender.getParam('output_folder').set(base_projects_dir)
    ntprender.getParam('output_production_folder').set(multi_project_dir)
    ntprender.getParam('job_name').set('multi_project: ' + user + ':' + project_name)
    ntprender.getParam('send_as_production').trigger()

    # chmod temporal
    os.system('chmod 777 -R ' + env.local)

    # guarda este proyecto para despues usarlo en 'send_to_render()'
    app1.saveProjectAs(submit_ntp)


def send_to_render():

    app_ = app1.loadProject(submit_ntp)

    videovina_node = get_videovina()
    vinarender = createNode('vinarender')
    vinarender.connectInput(0, videovina_node)

    vinarender.getParam('prefix').set(project_name)
    vinarender.getParam('project_folder').set(multi_project_dir)
    vinarender.getParam('job_name').set('videovina: ' + user + ':' + project_name)
    vinarender.getParam('filename').set(project_dir + '/renders/video.mov')

    vinarender.getParam('multi_project_render').trigger()


if action == 'create_multi_project':
    create_multi_project()
elif action == 'send_to_render':
    send_to_render()
