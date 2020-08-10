import os
import NatronEngine
from nx import getNode, alert, switch, get_connected_nodes, question, delete, warning, input_connected, dots_delete
from base import *
from vina import value_by_durations
from general import formats
from twelve_render import send_vinarender_state


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    children_refresh(thisParam, thisNode)
    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)
    if knob_name == 'render_shape':
        render(thisNode)
    if knob_name == 'read_file':
        read_file(thisNode, thisParam)
    if knob_name == 'clean':
        clean(thisNode)
    if knob_name == 'display_map':
        switch(
            thisNode,
            thisParam.get(),
            'Output',
            'switch',
            'start_frame_node'
        )


def clean(thisNode, dialog=True):
    def action():
        vinarender = getNode(thisNode, 'VinaRender')
        nodes = get_connected_nodes(vinarender)
        delete(nodes)
        dots_delete(thisNode)

    if dialog:
        if question("Esta seguro que desea borrar los nodos sobrantes ?", 'Limpiar Nodos'):
            action()
    else:
        action()


def read_file(thisNode, thisParam):
    twelve_read = getNode(thisNode, 'TwelveRead')
    twelve_read.getParam('reload').trigger()

    switch(
        thisNode,
        thisParam.get(),
        'start_frame_node',
        'VinaRender',
        'TwelveRead'
    )


def refresh(thisNode):
    current_speed = thisNode.getParam('speed').get()
    current_format = thisNode.getParam('format').get()
    durations = thisNode.getParam('durations').get()
    duration = thisNode.getParam('duration').get()
    duration = value_by_durations(duration, durations)[current_speed]

    switch_from_duration(thisNode, duration)

    # actualiza las transiciones de forma, solo si esta activado el 'read_file'
    read_file = thisNode.getParam('read_file').get()
    if not read_file:
        shape_transition_refresh(thisNode, current_speed, current_format)


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


def shape_transition_refresh(thisNode, speed=1, format=1):

    shape_format = getNode(thisNode, 'shape_format')

    _pixels = formats[format]
    shape_format.getParam('boxSize').set(_pixels[0], _pixels[0])

    # diferencias de tiempo que hay entre el shape de mascara y las de vidrio
    difference_with_mask = thisNode.getParam('difference_with_mask').get()

    durations = thisNode.getParam('durations').get()
    normal_duration = thisNode.getParam('duration').get()
    duration = value_by_durations(normal_duration, durations)[speed]
    mask_diff = value_by_durations(difference_with_mask, durations)[speed]

    # cambia el formato de 'OverlayMask'
    overlay_mask = getNode(thisNode, 'OverlayMask')
    overlay_mask.getParam('format').set(format)
    # ------------------------

    if not (normal_duration / 2) > difference_with_mask:
        alert('difference_with_mask: Este numero tiene que ser menor que el medio de la duracion.')
        return False

    for shape_name in ['shape_glass_1', 'shape_glass_2']:
        shape = getNode(thisNode, shape_name)
        shape.getParam('duration').set(duration)
        shape.getParam('format').set(format)
        shape.getParam('refresh').trigger()

    # la mascara de transicion tiene que ser con menor duracion que las otras formas
    transition_mask = getNode(thisNode, 'transition_mask')
    mask_duration = duration - mask_diff
    start_frame = 1
    if mask_diff:
        start_frame = mask_diff / 2

    transition_mask.getParam('duration').set(mask_duration)
    transition_mask.getParam('start_frame').set(start_frame)
    transition_mask.getParam('format').set(format)
    transition_mask.getParam('refresh').trigger()
    # ----------------------------------

    return True


def render(thisNode):
    vinarender = getNode(thisNode, 'VinaRender')
    duration = thisNode.getParam('duration').get()
    durations = thisNode.getParam('durations').get()
    prefix = thisNode.getParam('prefix').get()
    current_state = thisNode.getParam('current_state').get()

    if not input_connected(thisNode, 2):
        # verifica que el input de 'shape' este conectado
        warning('Shape', "El input 'Shape' no esta conectado.")
        return

    if current_state:
        _format = thisNode.getParam('format').get()
        speed = thisNode.getParam('speed').get()

        if shape_transition_refresh(thisNode, speed=speed, format=_format):
            send_vinarender_state(
                duration, durations, speed, prefix, _format, vinarender=vinarender)
        alert('Se envio a render el actual estado.')
    else:
        for speed in range(3):
            for _format in range(4):
                if shape_transition_refresh(thisNode, speed=speed, format=_format):
                    send_vinarender_state(
                        duration, durations, speed, prefix, _format, vinarender=vinarender)
                else:
                    break

        alert('Se enviaron a render las 12 diferentes transiciones.')
