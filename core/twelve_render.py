# Este plugin hace 9 renders con los distintos formatos y velocidades:
# HD Medio, Full Hd y 4K; Lento, Normal y Rapido
import os
import NatronEngine
from natron_utils import getNode, alert, value_by_speed, absolute


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'render':
        render(thisNode)
    if knob_name == 'render_slow':
        render(thisNode, 0)
    if knob_name == 'render_normal':
        render(thisNode, 1)
    if knob_name == 'render_fast':
        render(thisNode, 2)


def send_vinarender_state(duration, speeds, speed=1, prefix='render',
                          format=1, vinarender=False, thisNode=False):
    # ajusta los parametros de un nodo de videovina dependiendo de la velocidad y resolucion,
    # y luego lo envia a render

    prefix_dir = '[Project]/../footage/' + prefix
    absolule_path = absolute(prefix_dir)
    if not os.path.isdir(absolule_path):
        os.makedirs(absolule_path)

    last_frame = value_by_speed(duration, speeds)[speed]

    speeds_names = ['slow', 'normal', 'fast']
    formats_name = ['quarter', 'half', 'hd', '4k']

    speed_name = speeds_names[speed]
    format_name = formats_name[format]

    name = speed_name + '_' + format_name

    prefix_name = prefix + '_' + name
    render_dir = prefix_dir + '/' + prefix_name

    # si 'videovina' es 'False', busca el nodo, a partir de 'name'
    if not vinarender:
        vinarender = getNode(thisNode, name)
    # ----------------------

    vinarender.getParam('filename').set(
        render_dir + '/' + prefix_name + '_###.png')
    vinarender.getParam('job_name').set('glass_transition: ' + name)
    vinarender.getParam('no_dialog').set(True)
    vinarender.getParam('rgbonly').set(False)
    vinarender.getParam('instances').set(10)

    vinarender.getParam('range').set(1, last_frame)
    vinarender.getParam('render').trigger()


def render(thisNode, one_speed=None):
    prefix = thisNode.getParam('prefix').get()
    duration = thisNode.getParam('duration').get()
    speeds = thisNode.getParam('speeds').get()

    if not one_speed == None:
        speeds_list = [one_speed]
    else:
        speeds_list = range(3)

    for speed_index in speeds_list:
        for pixels_index in range(3):
            send_vinarender_state(duration, speeds, speed_index, prefix,
                                  pixels_index, thisNode=thisNode)

    if thisNode.getParam('dialog').get():
        alert('Se enviaron a render las 9 diferentes transiciones.')
