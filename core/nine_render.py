# Este plugin hace 9 renders con los distintos formatos y velocidades:
# HD Medio, Full Hd y 4K; Lento, Normal y Rapido
import os
import NatronGui
import NatronEngine
from natron_utils import getNode, alert, duration_by_speed

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'render':
        render(thisNode)

def render(thisNode):
    prefix = thisNode.getParam('prefix').get()

    resolutions = ['mid', 'hd', '4k']
    speeds = ['slow', 'normal', 'fast']

    for velocity_index, velocity in enumerate(speeds):
        duration = thisNode.getParam('duration').get()
        speeds = thisNode.getParam('speeds').get()
        last_frame = duration_by_speed(duration, speeds)[velocity_index]

        for resolution in resolutions:
            name = velocity + '_' + resolution

            render_node = getNode(thisNode, name)

            render_dir = prefix + '_' + name 

            render_node.getParam('filename').set(render_dir + '/' + name + '_###.jpg')
            render_node.getParam('job_name').set( 'glass_transition: ' + name)
            render_node.getParam('no_dialog').set(True)
            render_node.getParam('rgbonly').set(True)

            render_node.getParam('range').set(1, last_frame)
            
            render_node.getParam('render').trigger()

    if thisNode.getParam('dialog').get():
        alert('Se enviaron a render las 9 diferentes transiciones.')