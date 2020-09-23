# Este plugin hace 12 renders con los distintos formatos y velocidades:
# HD Medio, Full Hd y 4K; Lento, Normal y Rapido
import os
import NatronEngine
from nx import getNode, alert, absolute, createNode, node_delete, get_connected_nodes
from vina import value_by_durations
from general import formats
from base import link_to_parent


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'render':
        render(thisNode)
    if knob_name == 'link_to_connected':
        link_to_connected(thisNode)


def send_vinarender_state(durations, speed=1, prefix='render', format=1, vinarender=False, thisNode=False):
    # ajusta los parametros de un nodo de videovina dependiendo de
    # la velocidad y resolucion, luego lo envia a render.

    refresh_connected_nodes(thisNode, speed, format)

    prefix_dir = '[Project]/../footage/' + prefix
    absolule_path = absolute(prefix_dir)
    if not os.path.isdir(absolule_path):
        os.makedirs(absolule_path)

    speeds_names = ['slow', 'normal', 'fast']
    formats_name = ['quarter', 'half', 'hd', '4k']

    speed_name = speeds_names[speed]
    format_name = formats_name[format]

    name = speed_name + '_' + format_name

    prefix_name = prefix + '_' + name
    render_dir = prefix_dir + '/' + prefix_name

    image_input = getNode(thisNode, 'Image_4K')

    # reformat node
    reformat_name = 'reformat_' + name
    reformat = getNode(thisNode, reformat_name)

    if not reformat:
        reformat = createNode('reformat', reformat_name, thisNode)
        reformat.getParam('reformatType').set(1)
        reformat.getParam('boxFixed').set(True)

        _format = formats[format]
        reformat.getParam('boxSize').set(_format[0], _format[1])

        reformat.connectInput(0, image_input)

    # Filtro para el reformat
    filter_param = thisNode.getParam('filter')
    reformat_filter = filter_param.getOption(filter_param.get())
    filters_index = {'Cubic': 3, 'Impulse': 0, 'Notch': 9}
    reformat.getParam('filter').set(filters_index[reformat_filter])

    # vinarender node
    vinarender = getNode(thisNode, name)

    if not vinarender:
        vinarender = createNode('vinarender', name, thisNode)
        vinarender.connectInput(0, reformat)

    sequence_type = thisNode.getParam('sequence_type').get()
    ext = ['png', 'jpg'][sequence_type]

    if ext == 'png':
        vinarender.getParam('rgbonly').set(False)
    else:
        vinarender.getParam('rgbonly').set(True)

    vinarender.getParam('filename').set(render_dir + '/' + prefix_name + '_####.' + ext)
    vinarender.getParam('job_name').set(prefix + ': ' + name)
    vinarender.getParam('no_show_message').set(True)
    vinarender.getParam('instances').set(10)
    vinarender.getParam('range').set(1, durations[speed])
    vinarender.getParam('render').trigger()

    node_delete(vinarender)
    node_delete(reformat)


def refresh_connected_nodes(thisNode, speed, format):
    # Actaualiza todos los nodos que de que tengan los atributos de videovina
    # a la velocidad correspondiente.
    thisNode.format.set(format)
    thisNode.speed.set(speed)

    connected_nodes = get_connected_nodes(thisNode, parent_include=False)
    for node in connected_nodes:
        refresh_param = node.getParam('refresh')

        if not refresh_param:
            continue

        refresh_param.trigger()


def link_to_connected(thisNode):

    connected_nodes = get_connected_nodes(thisNode, parent_include=False)

    for node in connected_nodes:
        link_to_parent(node, thisNode, thisNode, force=True)


def render(thisNode):

    if not thisNode.getInput(0):
        alert('Debe conectar la imagen 4K')
        return

    current_state = thisNode.getParam('current_state').get()
    current_speed_render = thisNode.getParam('current_speed').get()
    prefix = thisNode.getParam('prefix').get()
    durations = thisNode.getParam('durations').get()

    current_format = thisNode.getParam('format').get()
    current_speed = thisNode.getParam('speed').get()

    if current_state:
        send_vinarender_state(durations, current_speed, prefix, current_format, thisNode=thisNode)
    elif current_speed_render:
        for format_index in range(3):
            send_vinarender_state(durations, current_speed, prefix, format_index + 1, thisNode=thisNode)
    else:
        for speed in range(3):
            for format_index in range(3):
                send_vinarender_state(durations, speed, prefix, format_index + 1, thisNode=thisNode)
