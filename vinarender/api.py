# api: este archivo permite subministrar un proyecto videovina,
# que se envio desde el editor web de videovina.
from nx import createNode, saveProject
from vina import get_videovina
import json
import os
import shutil
from sys import argv
from util import fread, jread, jwrite, makedirs


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
    user_id = data['user_id']
    _format = data['format']

    public_project_dir = env.s3 + '/public/' + user_id + '/projects/' + project_name
    private_project_dir = env.s3 + '/private/' + user + '/projects/' + project_name
    videovina_project = private_project_dir + '/project.json'
    base_projects_dir = env.assets + '/templates_base/' + project_type + '/comp/ntp'  # Remplazar 'templates_base' solo por 'templates'

    # Copia footage, project.json de amazon S3 y lo copia en el directorio compartido local
    project_json = project_dir + '/project.json'
    shutil.copy(videovina_project, project_json)

    # se suman algunos datos adicionales al proyecto json copiado a local
    project_data = jread(project_json)
    project_data.format = _format
    project_data.user_id = user_id
    jwrite(project_json, project_data)

    s3_footage = private_project_dir + '/footage'
    loal_footage = project_dir + '/footage'
    makedirs(loal_footage)
    # copia las fotos de a una, por si ya estan en el directorio local
    # asi no se gasta tanto trafico
    for photo in os.listdir(s3_footage):
        src = s3_footage + '/' + photo
        dst = loal_footage + '/' + photo
        if not os.path.isfile(dst):
            shutil.copy(src, dst)

    # copia las fuente al directorio local
    fonts_dir = public_project_dir + '/fonts'
    if os.path.isdir(fonts_dir):
        shutil.copytree(fonts_dir, project_dir + '/fonts')

    # copia las canciones
    song = project_data.states.app.song + '.mp3'
    song_src = private_project_dir + '/songs/' + song
    if os.path.isfile(song_src):
        shutil.copy(song_src, project_dir + '/' + song)

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
    vinarender.getParam('instances').set(4)
    vinarender.getParam('job_name').set('videovina: ' + user + ':' + project_name)
    vinarender.getParam('filename').set(project_dir + '/renders/video.mp4')
    vinarender.getParam('video_format').set(1)
    vinarender.getParam('output_quality').set(0)

    vinarender.getParam('multi_project_render').trigger()

    app1.saveProject(submit_ntp)


if action == 'create_multi_project':
    create_multi_project()
elif action == 'send_to_render':
    send_to_render()
