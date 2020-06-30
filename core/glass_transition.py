import os
import NatronGui
import NatronEngine
from natron_utils import getNode, alert, value_by_speed, switch, get_connected_nodes, question, delete
from general import formats
from nine_render import send_vinarender_state


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)
    if knob_name == 'render_shape':
        render(thisNode)
    if knob_name == 'read_file':
        read_file(thisNode, thisParam)
    if knob_name == 'clean':
        clean(thisNode, app)
    if knob_name == 'display_map':
        switch(
            thisNode,
            thisParam.get(),
            'Output',
            'switch',
            'start_frame_node'
        )


def clean(thisNode, app):
    vinarender = getNode(thisNode, 'VinaRender')
    if question("Esta seguro que desea borrar los nodos sobrantes ?", 'Limpiar Nodos'):
        nodes = get_connected_nodes(vinarender)
        delete(nodes)


def read_file(thisNode, thisParam):
    nine_read = getNode(thisNode, 'NineRead')
    nine_read.getParam('reload').trigger()

    switch(
        thisNode,
        thisParam.get(),
        'start_frame_node',
        'VinaRender',
        'NineRead'
    )


def refresh(thisNode):

    current_speed = thisNode.getParam('speed').get()
    current_resolution = thisNode.getParam('resolution').get()
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
        shape_transition_refresh(thisNode, current_speed, current_resolution)


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


def shape_transition_refresh(thisNode, speed=1, pixels=1):

    shape_format = getNode(thisNode, 'shape_format')

    _pixels = formats[pixels]
    shape_format.getParam('boxSize').set(_pixels[0], _pixels[0])

    # diferencias de tiempo que hay entre el shape de mascara y las de vidrio
    difference_with_mask = thisNode.getParam('difference_with_mask').get()

    speeds = thisNode.getParam('speeds').get()
    normal_duration = thisNode.getParam('duration').get()
    duration = value_by_speed(normal_duration, speeds)[speed]
    mask_diff = value_by_speed(difference_with_mask, speeds)[speed]

    # cambia la resolucion de 'OverlayMask'
    overlay_mask = getNode(thisNode, 'OverlayMask')
    rscale = _pixels[0] / float(formats[1][0])
    overlay_mask.getParam('rscale').set(rscale)
    # ------------------------

    if not (normal_duration / 2) > difference_with_mask:
        alert('difference_with_mask: Este numero tiene que ser menor que el medio de la duracion.')
        return False

    for shape_name in ['shape_glass_1', 'shape_glass_2']:
        shape = getNode(thisNode, shape_name)
        shape.getParam('duration').set(duration)
        shape.getParam('formatboxSize').set(_pixels[0], _pixels[1])
        shape.getParam('refresh').trigger()

    # la mascara de transicion tiene que ser con menor duracion que las otras formas
    transition_mask = getNode(thisNode, 'transition_mask')
    mask_duration = duration - mask_diff
    start_frame = 1
    if mask_diff:
        start_frame = mask_diff / 2

    transition_mask.getParam('duration').set(mask_duration)
    transition_mask.getParam('start_frame').set(start_frame)
    transition_mask.getParam('formatboxSize').set(
        _pixels[0], _pixels[1])
    transition_mask.getParam('refresh').trigger()
    # ----------------------------------

    return True


def render(thisNode):
    vinarender = getNode(thisNode, 'VinaRender')
    duration = thisNode.getParam('duration').get()
    speeds = thisNode.getParam('speeds').get()
    prefix = thisNode.getParam('prefix_render').get()
    current_state = thisNode.getParam('current_state').get()

    if current_state:
        pixels = thisNode.getParam('resolution').get()
        speed = thisNode.getParam('speed').get()

        if shape_transition_refresh(thisNode, speed=speed, pixels=pixels):
            send_vinarender_state(
                duration, speeds, speed, prefix, pixels, vinarender=vinarender)
        alert('Se enviaron a render el actual estado.')
    else:
        for speed in range(3):
            for pixels in range(3):
                if shape_transition_refresh(thisNode, speed=speed, pixels=pixels):
                    send_vinarender_state(
                        duration, speeds, speed, prefix, pixels, vinarender=vinarender)
                else:
                    break

        alert('Se enviaron a render las 9 diferentes transiciones.')
