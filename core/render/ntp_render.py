import NatronEngine
from natron_extent import *
from base import *
import os


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    name = thisParam.getScriptName()

    if name == 'send':
        render(thisNode)


def render(thisNode):
    output_folder = thisNode.getParam('output_folder').get()
    output_folder = absolute(output_folder)

    instances = thisNode.getParam('instances').get()
    slides_count = thisNode.getParam('slides_count').get()
    slides_by_project = thisNode.getParam('slides_by_project').get()

    name = get_project_name()
    for i in range(slides_count):

        project_folder = output_folder + '/' + name + '_' + str(i + 1) + '-slides'
        if not os.path.isdir(project_folder):
            os.makedirs(project_folder)
