# Este plugin hace 9 renders con los distintos formatos y velocidades:
# HD Medio, Full Hd y 4K; Lento, Normal y Rapido
import os
import NatronGui
import NatronEngine
from natron_utils import getNode, alert, value_by_speed, absolute

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'render':
        render(thisNode)
    if knob_name == 'render_slow':
        render(thisNode, 'slow')
    if knob_name == 'render_normal':
        render(thisNode, 'normal')
    if knob_name == 'render_fast':
        render(thisNode, 'fast')

def render(thisNode, one_speed = False):
    prefix = thisNode.getParam('prefix').get()
    prefix_dir = thisNode.getParam('prefix_dir').get() + '/' + prefix 
    absolule_path = absolute(prefix_dir)

    if not os.path.isdir(absolule_path):
        os.makedirs(absolule_path)
     
    speeds_names = ['slow', 'normal', 'fast']
    resolutions = ['mid', 'hd', '4k']

    if one_speed:
        speeds_list = [one_speed]
    else:
        speeds_list = speeds_names
        
    for velocity in speeds_list:
        duration = thisNode.getParam('duration').get()
        speeds = thisNode.getParam('speeds').get()

        velocity_index = speeds_names.index(velocity)
        last_frame = value_by_speed(duration, speeds)[velocity_index]

        for resolution in resolutions:
            name = velocity + '_' + resolution
            render_node = getNode(thisNode, name)

            prefix_name = prefix + '_' + name
            render_dir = prefix_dir + '/' + prefix_name 

            render_node.getParam('filename').set(render_dir + '/' + prefix_name + '_###.png')
            render_node.getParam('job_name').set( 'glass_transition: ' + name)
            render_node.getParam('no_dialog').set(True)
            render_node.getParam('rgbonly').set(False)

            render_node.getParam('range').set(1, last_frame)
            render_node.getParam('render').trigger()

    if thisNode.getParam('dialog').get():
        alert('Se enviaron a render las 9 diferentes transiciones.')