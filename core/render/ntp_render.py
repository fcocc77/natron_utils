import NatronEngine
from natron_extent import *
from base import *
import os


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
    first_slide = 1
    for i in range(slides_count + 1):

        if (count > slides_by_project - 1) or (slides_count == i):
            first = (first_slide - 1) - 1
            last = (i - 1) + 1

            if first < 0:
                first = 0

            tasks.append((first, last))
            first_slide = i + 1
            count = 0

        count += 1
    # -------------------------------
    print tasks

    return tasks


def render(thisNode, app):
    output_folder = thisNode.getParam('output_folder').get()
    output_folder = absolute(output_folder)

    instances = thisNode.getParam('instances').get()
    slides_count = thisNode.getParam('slides_count').get()
    slides_by_project = thisNode.getParam('slides_by_project').get()

    project_name = app.projectName.get()
    job_name = thisNode.job_name.get()
    if not job_name:
        job_name = project_name.split('.')[0]

    server_group = 'Natron'
    software = 'Ntp'

    get_tasks(slides_count, slides_by_project)

    # name = get_project_name()
    # for i in range(slides_count):

    #     project_folder = output_folder + '/' + name + '_' + str(i + 1) + '-slides'
    #     if not os.path.isdir(project_folder):
    #         os.makedirs(project_folder)

    # cmd = (submit
    #        + ' -jobName "' + job_name + '"'
    #        + ' -serverGroup ' + server_group
    #        + ' -firstFrame ' + str(1)
    #        + ' -lastFrame ' + str(1)
    #        + ' -taskSize ' + str(task_size)
    #        + ' -project "' + project + '"'
    #        + ' -software ' + software
    #        + ' -render ' + render
    #        + ' -extra ' + output
    #        + ' -instances ' + str(instances)
    #        )
