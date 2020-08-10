from nx import getNode
from vina import value_by_durations
import NatronEngine
from base import link_to_parent


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return
    knob_name = thisParam.getScriptName()

    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def animation(param, values, start_frame, duration, dimension=0):
    value_a = float(values[0])
    value_b = float(values[1])

    first_frame = start_frame
    last_frame = first_frame + duration

    param.setValueAtTime(value_a, first_frame, dimension)
    param.setValueAtTime(value_b, last_frame, dimension)

    horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal
    param.setInterpolationAtTime(first_frame,  horizontal, dimension)
    param.setInterpolationAtTime(last_frame,  horizontal, dimension)


def refresh(thisNode):
    transform = getNode(thisNode, 'transform')
    translate = transform.getParam('translate')

    rectangle = getNode(thisNode, 'rectangle')
    bottom_left = rectangle.getParam('bottomLeft')
    size = rectangle.getParam('size')

    rscale = thisNode.getParam('rscale').get()
    start_frame = thisNode.getParam('start_frame').get()
    speed = thisNode.getParam('speed').get()
    input_box = thisNode.getParam('input_box').get()
    output_box = thisNode.getParam('output_box').get()
    duration = thisNode.getParam('duration').get()
    durations = thisNode.getParam('durations').get()
    transition_duration_percent = thisNode.getParam(
        'transition_duration').get()
    width_box = thisNode.getParam('width').get() * rscale
    height_box = thisNode.getParam('height').get() * rscale

    current_format = thisNode.getParam('current_format').get()
    width = current_format[0]
    height = current_format[1]

    # restaurar valores
    size.restoreDefaultValue(0)
    size.restoreDefaultValue(1)
    bottom_left.restoreDefaultValue(0)
    bottom_left.restoreDefaultValue(1)
    translate.restoreDefaultValue(0)
    translate.restoreDefaultValue(1)

    # calcular el centro
    center = (width / 2) - (width_box / 2)

    bottom_left.set(center, 0)

    size.set(width_box, 1080)

    # calcula la duracion de la transicion
    transition_duration = (transition_duration_percent * duration) / 100

    height_box = (height * height_box) / 100
    value_a_bottom_left = height / 2
    value_b_bottom_left = (height - height_box) / 2

    value_x = (width / 2) + (width_box / 2)

    # transicion de entrada
    if input_box == 0:
        animation(translate, [-value_x, 0], start_frame,
                  transition_duration, dimension=0)
    elif input_box == 1:
        animation(translate, [value_x, 0], start_frame,
                  transition_duration, dimension=0)

    elif input_box == 4:
        animation(size, [0, height_box], start_frame,
                  transition_duration, dimension=1)

        animation(bottom_left, [value_a_bottom_left, value_b_bottom_left], start_frame,
                  transition_duration, dimension=1)

    # transicion de salida
    start_frame_output = duration - transition_duration
    if output_box == 0:
        animation(translate, [0, -value_x], start_frame_output,
                  transition_duration, dimension=0)
    elif output_box == 1:
        animation(translate, [0, value_x], start_frame_output,
                  transition_duration, dimension=0)

    elif output_box == 4:

        animation(size, [height_box, 0], start_frame_output,
                  transition_duration, dimension=1)

        animation(bottom_left, [value_b_bottom_left, value_a_bottom_left],
                  start_frame_output, transition_duration, dimension=1)
