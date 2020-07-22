import NatronEngine
import os
from nx import get_project_name, get_project_path, absolute, alert, saveProject
import json


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    name = thisParam.getScriptName()

    if name == 'send':
        render(thisNode, app)


def get_tasks(slides_count, slides_by_project):
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
                'slides': (first_slide, last_slide),
                'range': (first_slide_orginal, last_slide_original),
            })
            start_slide = i + 1
            count = 0

        count += 1
    # -------------------------------
    return tasks


def render(thisNode, app):
    output_folder = thisNode.getParam('output_folder').get()
    output_folder = absolute(output_folder)

    instances = thisNode.getParam('instances').get()
    slides_count = thisNode.getParam('slides_count').get()
    slides_by_project = thisNode.getParam('slides_by_project').get()

    job_name = thisNode.job_name.get()
    if not job_name:
        job_name = get_project_name()

    server_group = 'Natron'
    software = 'Ntp'
    submit = '/opt/vinarender/bin/submit'

    tasks = get_tasks(slides_count, slides_by_project)

    first_slide = 0
    last_slide = len(tasks) - 1

    saveProject()

    cmd = (submit
           + ' -jobName "' + job_name + '"'
           + ' -serverGroup ' + server_group
           #    first_frame last_frame equivalen al primer y ultimo slide
           + ' -firstFrame ' + str(first_slide)
           + ' -lastFrame ' + str(last_slide)
           #    ------------------------
           + ' -taskSize ' + str(1)
           + ' -project "' + get_project_path() + '"'
           + ' -software ' + software
           + ' -render "' + output_folder + '"'
           + ' -extra \'' + json.dumps(tasks) + "'"
           + ' -instances ' + str(instances)
           )
    os.system(cmd)

    alert('Render Sended.', 'VinaRender')
