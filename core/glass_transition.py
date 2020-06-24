import os
import NatronGui
import NatronEngine
from natron_utils import getNode, alert

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'render_shape':
        render(thisNode)

def render(thisNode):

    prefix = thisNode.getParam('prefix_transition_file').get()

    list_renders = ['slow_mid', 'slow_hd', 'slow_4k', 'normal_mid', 'normal_hd', 'normal_4k', 'fast_mid', 'fast_hd', 'fast_4k']

    for name in list_renders:
        render_node = getNode(thisNode, name)

        render_dir = prefix + '_' + name 

        render_node.getParam('filename').set(render_dir + '/' + name + '_###.jpg')
        render_node.getParam('job_name').set( 'glass_transition: ' + name)
        render_node.getParam('no_dialog').set(True)
        render_node.getParam('rgbonly').set(True)

        last_frame = thisNode.getParam('duration').get()

        render_node.getParam('range').set(1, last_frame)

        render_node.getParam('render').trigger()

    alert('Se enviaron a render las 9 diferentes transiciones.')