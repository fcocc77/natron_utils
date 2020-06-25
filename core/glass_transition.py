import os
import NatronGui
import NatronEngine
from natron_utils import getNode, alert, duration_by_speed

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'render_shape':
        render(thisNode)

def render(thisNode):

    nine_render = getNode(thisNode, 'NineRender')

    speeds = thisNode.getParam('speeds').get()
    normal_duration = thisNode.getParam('duration').get()
    
    render_speeds = ['render_slow', 'render_normal', 'render_fast']

    for render_speed, duration in zip(render_speeds, duration_by_speed(normal_duration, speeds)):

        for shape_name in ['shape1','shape2','shape3']:
            shape = getNode(thisNode, shape_name)
            shape.getParam('duration').set(duration)
            shape.getParam('refresh').trigger()

        nine_render.getParam(render_speed).trigger()

    alert('Se enviaron a render las 9 diferentes transiciones.')