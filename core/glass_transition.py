import os
import NatronGui
import NatronEngine
from natron_utils import getNode, alert, value_by_speed

def main(thisParam, thisNode, thisGroup, app, userEdited):
    knob_name = thisParam.getScriptName()

    if knob_name == 'render_shape':
        render(thisNode)

def render(thisNode):

    # diferencias de tiempo que hay entre el shape de mascara y las de vidrio
    difference_with_mask = thisNode.getParam('difference_with_mask').get()

    nine_render = getNode(thisNode, 'NineRender')

    speeds = thisNode.getParam('speeds').get()
    normal_duration = thisNode.getParam('duration').get()
    
    render_speeds = ['render_slow', 'render_normal', 'render_fast']
    durations = value_by_speed(normal_duration, speeds)
    masks_diff = value_by_speed(difference_with_mask, speeds)

    for render_speed, duration, mask_diff in zip(render_speeds, durations, masks_diff):

        for shape_name in ['shape_glass_1','shape_glass_2']:
            shape = getNode(thisNode, shape_name)
            shape.getParam('duration').set(duration)
            shape.getParam('refresh').trigger()

        # la mascara de transicion tiene que ser con menor duracion que las otras formas
        transition_mask = getNode(thisNode, 'transition_mask')
        mask_duration = duration - mask_diff
        start_frame = 1
        if mask_diff:
            start_frame = mask_diff / 2
        
        transition_mask.getParam('duration').set(mask_duration)
        transition_mask.getParam('start_frame').set(start_frame)
        transition_mask.getParam('refresh').trigger()
        # ----------------------------------

        nine_render.getParam(render_speed).trigger()

    alert('Se enviaron a render las 9 diferentes transiciones.')