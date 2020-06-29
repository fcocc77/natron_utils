import os
from natron_utils import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'reload' or knob_name == 'velocity' or knob_name == 'resolution':
        reload_file(thisNode)


def reload_file(thisNode):
    read = getNode(thisNode, 'read')

    resolutions = ['mid', 'hd', '4k']
    speeds = ['slow', 'normal', 'fast']

    velocity = thisNode.getParam('velocity').get()
    resolution = thisNode.getParam('resolution').get()

    current_velocity = speeds[velocity]
    current_resolution = resolutions[resolution]

    prefix = thisNode.getParam('prefix').get()

    prefix_name = prefix + '_' + current_velocity + '_' + current_resolution

    filename_param = read.getParam('filename')
    filename = thisNode.getParam('prefix_dir').get(
    ) + '/' + prefix + '/' + prefix_name + '/' + prefix_name + '_###.png'

    if filename_param.get() == filename:
        filename_param.reloadFile()
    else:
        filename_param.set(filename)

    read.getParam('outputPremult').set(0)
