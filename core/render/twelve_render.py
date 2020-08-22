# Este plugin hace 12 renders con los distintos formatos y velocidades:
# HD Medio, Full Hd y 4K; Lento, Normal y Rapido
import os
import NatronEngine
from nx import getNode, alert, absolute, createNode
from vina import value_by_durations
from general import formats


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'render':
        render(thisNode)


def send_vinarender_state(durations, speed=1, prefix='render', format=1, vinarender=False, thisNode=False):
    # ajusta los parametros de un nodo de videovina dependiendo de
    # la velocidad y resolucion, luego lo envia a render.

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

    # vinarender node
    vinarender = getNode(thisNode, name)

    if not vinarender:
        vinarender = createNode('vinarender', name, thisNode)
        vinarender.connectInput(0, reformat)

    vinarender.getParam('filename').set(render_dir + '/' + prefix_name + '_###.png')
    vinarender.getParam('job_name').set(prefix + ': ' + name)
    vinarender.getParam('rgbonly').set(False)
    vinarender.getParam('no_show_message').set(True)
    vinarender.getParam('instances').set(10)
    vinarender.getParam('range').set(1, durations[speed])
    vinarender.getParam('render').trigger()


def refresh_source_speed(thisNode, speed):
    # Actaualiza el nodo que se va a renderizar, a la velocidad correspondiente.

    source_node = thisNode.getInput(0)
    speed_param = source_node.getParam('speed')
    refresh_param = source_node.getParam('refresh')

    if not speed_param:
        alert('El nodo conectado debe tener el parametro de "speed"')
        return False

    speed_param.set(speed)
    refresh_param.trigger()

    return True


def render(thisNode):

    if not thisNode.getInput(0):
        alert('Debe conectar la imagen 4K')
        return

    current_state = thisNode.getParam('current_state').get()
    prefix = thisNode.getParam('prefix').get()
    durations = thisNode.getParam('durations').get()

    current_format = thisNode.getParam('format').get()
    current_speed = thisNode.getParam('speed').get()

    if current_state:
        if not refresh_source_speed(thisNode, current_speed):
            return
        send_vinarender_state(durations, current_speed, prefix, current_format, thisNode=thisNode)
    else:
        for speed in range(3):
            if not refresh_source_speed(thisNode, speed):
                return

            for format_index in range(3):
                send_vinarender_state(durations, speed, prefix, format_index + 1, thisNode=thisNode)
