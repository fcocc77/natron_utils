import NatronEngine
import os
import shutil
from nx import get_project_name, get_project_path, absolute, alert, saveProject, warning
import json
from api import get_videovina_project
from vina import videovina_data


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    name = thisParam.getScriptName()

    if name == 'send':
        generate_base_projects(thisNode, app)

    if name == 'send_as_production':
        generate_render_projects(thisNode, app)


def generate_render_projects(thisNode, app):
    output = thisNode.getParam('output_production_folder').get()
    source_folder = thisNode.getParam('output_folder').get()

    videovina_node = thisNode.getInput(0)
    if not videovina_node:
        warning('NtpRender', '!You must connect the VideoVina Node.')
        return

    send_as_production(thisNode, absolute(source_folder), absolute(output))


def send_as_production(thisNode, source, output):
    vina = videovina_data()

    if os.path.isdir(output):
        shutil.rmtree(output)
    os.makedirs(output)

    # crea lista con los proyectos necesarios para la cantidad de slides a renderizar
    last_slide = vina.total_slides - 1

    required_slides = []
    for ntp in os.listdir(source):
        ext = ntp[-3:]
        if ext == 'ntp':
            slide_range = ntp.split('_')[-1].split('.ntp')[0]
            first_frame = int(slide_range.split('-')[0])
            last_frame = int(slide_range.split('-')[-1])

            if last_frame <= vina.total_slides + 1:
                last_project = False
                if last_slide >= first_frame and last_slide <= last_frame:
                    last_project = True

                required_slides.append([ntp, last_project])
    # -----------------------------

    tasks = []
    for project, last_project in required_slides:
        shutil.copy(source + '/' + project, output)

        tasks.append({
            'module': 'production_ntp',
            'project': output + '/' + project,
            'last_project': last_project,
            'last_slide': last_slide,
            'speed': vina.speed,
            'format': vina.format
        })

    render(thisNode, tasks)


def get_tasks(slides_count, slides_by_project, output_folder, project):
    # calcula cuantas tareas tiene que tener vinarender dependiendo
    # de la cantidad de 'slides' y las 'slides por proyecto'.

    # crea una lista de rangos, dandole 1 slide antes y despues del rango
    tasks = []
    count = 0
    start_slide = 1
    for i in range(slides_count + 1):
        if (count > slides_by_project - 1) or (slides_count == i):
            first_slide = start_slide - 1
            first_slide_orginal = first_slide

            last_slide = i - 1
            last_slide_original = last_slide

            # le agrega 1 slide al principio y al final, solo si no es el primer o el ultimo slide
            first_slide -= 1
            if first_slide < 0:
                first_slide = 0
                first_slide_orginal = 0

            last_slide += 1
            if last_slide == slides_count:
                last_slide -= 1
            # ----------------

            tasks.append({
                'module': 'ntp',
                'slides': (first_slide, last_slide),
                'range': (first_slide_orginal, last_slide_original),
                'project': project,
                'output_folder': output_folder
            })
            start_slide = i + 1
            count = 0

        count += 1
    # -------------------------------
    return tasks


def generate_base_projects(thisNode, app):
    output_folder = thisNode.getParam('output_folder').get()
    output_folder = absolute(output_folder)

    slides_count = thisNode.getParam('slides_count').get()
    slides_by_project = thisNode.getParam('slides_by_project').get()
    tasks = get_tasks(
        slides_count,
        slides_by_project,
        output_folder,
        get_project_path()
    )

    render(thisNode, tasks)


def render(thisNode, extra):
    instances = thisNode.getParam('instances').get()

    job_name = thisNode.job_name.get()
    if not job_name:
        job_name = get_project_name()

    server_group = 'Natron'
    software = 'Ntp'
    submit = '/opt/vinarender/bin/submit'

    first_slide = 0
    last_slide = len(extra) - 1

    saveProject()

    cmd = (submit
           + ' -jobName "' + job_name + '"'
           + ' -serverGroup ' + server_group
           #    first_frame last_frame equivalen al primer y ultimo slide
           + ' -firstFrame ' + str(first_slide)
           + ' -lastFrame ' + str(last_slide)
           #    ------------------------
           + ' -taskSize ' + str(1)
           + ' -software ' + software
           + ' -extra \'' + json.dumps(extra) + "'"
           + ' -instances ' + str(instances)
           )
    os.system(cmd)

    alert('Render Sended.', 'VinaRender')
