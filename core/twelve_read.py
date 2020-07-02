import os
from natron_extent import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'reload' or knob_name == 'speed' or knob_name == 'format':
        reload_file(thisNode)


def reload_file(thisNode):
    read = getNode(thisNode, 'read')

    formats_name = ['quarter', 'half', 'hd', '4k']
    speeds = ['slow', 'normal', 'fast']

    speed = thisNode.getParam('speed').get()
    format = thisNode.getParam('format').get()

    current_speed = speeds[speed]
    current_format = formats_name[format]

    prefix = thisNode.getParam('prefix').get()

    prefix_name = prefix + '_' + current_speed + '_' + current_format

    filename_param = read.getParam('filename')
    filename = '[Project]/../footage/' + prefix + '/' + \
        prefix_name + '/' + prefix_name + '_###.png'

    if filename_param.get() == filename:
        filename_param.reloadFile()
    else:
        filename_param.set(filename)

    read.getParam('outputPremult').set(0)
