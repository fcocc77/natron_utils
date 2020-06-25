import os
from natron_utils import getNode

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'reload':
        reload_file(thisNode)

def reload_file(thisNode):
    read = getNode(thisNode, 'read')

    resolutions = ['mid', 'hd', '4k']
    speeds = ['slow', 'normal', 'fast']

    velocity = thisNode.getParam('velocity').get()
    resolution = thisNode.getParam('resolution').get()

    current_velocity = speeds[velocity]
    current_resolution = resolutions[resolution]

    prefix_name = thisNode.getParam('prefix').get() + '_' + current_velocity + '_' + current_resolution

    filename = thisNode.getParam('prefix_dir').get() + '/' + prefix_name + '/' + prefix_name + '.jpg'
    read.getParam('filename').set(filename)