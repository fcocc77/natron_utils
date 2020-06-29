import os
import NatronGui
import NatronEngine
from natron_utils import getNode, alert, value_by_speed, switch


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)
    if knob_name == 'speed':
        refresh(thisNode)
    if knob_name == 'resolution':
        refresh(thisNode)
    if knob_name == 'render_shape':
        render(thisNode)
    if knob_name == 'read_file':
        read_file(thisNode, thisParam)

    if knob_name == 'display_map':
        switch(
            thisNode,
            thisParam.get(),
            'Output',
            'switch',
            'start_frame_node'
        )


def read_file(thisNode, thisParam):
    nine_read = getNode(thisNode, 'NineRead')
    nine_read.getParam('reload').trigger()

    switch(
        thisNode,
        thisParam.get(),
        'start_frame_node',
        'NineRender',
        'NineRead'
    )


def refresh(thisNode):

    current_speed = thisNode.getParam('speed').get()
    speeds = thisNode.getParam('speeds').get()
    duration = thisNode.getParam('duration').get()
    duration = value_by_speed(duration, speeds)[current_speed]

    # recargar nine read
    nine_read = getNode(thisNode, 'NineRead')
    nine_read.getParam('reload').trigger()

    switch_from_duration(thisNode, duration)

    # actualiza las transiciones de forma, solo si esta activado el 'read_file'
    read_file = thisNode.getParam('read_file').get()
    if not read_file:
        shape_transition_refresh(thisNode, current_speed)


def switch_from_duration(thisNode, duration):
    # hace un switch, dejando dentro del rango de duracion el fx de vidrio,
    # asi no carga el efecto fuera de ese rango.
    switch = getNode(thisNode, 'switch').getParam('which')
    first_frame = thisNode.getParam('start_frame').get()
    last_frame = first_frame + duration

    switch.restoreDefaultValue()

    switch.setValueAtTime(0, first_frame - 1)
    switch.setValueAtTime(1, first_frame)
    switch.setValueAtTime(2, last_frame + 1)


def shape_transition_refresh(thisNode, speed=1):

    # diferencias de tiempo que hay entre el shape de mascara y las de vidrio
    difference_with_mask = thisNode.getParam('difference_with_mask').get()

    speeds = thisNode.getParam('speeds').get()
    normal_duration = thisNode.getParam('duration').get()
    duration = value_by_speed(normal_duration, speeds)[speed]
    mask_diff = value_by_speed(difference_with_mask, speeds)[speed]

    if not (normal_duration / 2) > difference_with_mask:
        alert('difference_with_mask: Este numero tiene que ser menor que el medio de la duracion.')
        return False

    for shape_name in ['shape_glass_1', 'shape_glass_2']:
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

    return True


def render(thisNode):
    nine_render = getNode(thisNode, 'NineRender')
    nine_render.getParam('dialog').set(False)

    render_speeds = ['render_slow', 'render_normal', 'render_fast']

    for i, render_speed in enumerate(render_speeds):
        if shape_transition_refresh(thisNode, speed=i):
            nine_render.getParam(render_speed).trigger()
        else:
            break

    alert('Se enviaron a render las 9 diferentes transiciones.')
