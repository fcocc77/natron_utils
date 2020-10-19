from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, get_durations
from nx import getNode
from vina import value_by_durations
import random


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):

    current_format = get_format(thisNode)

    transform = getNode(thisNode, 'transform')

    translate = transform.getParam('translate')
    center = transform.getParam('center')
    scale = transform.getParam('scale')
    rotate = transform.getParam('rotate')

    frequency = thisNode.frequency.get()

    center.set(current_format[0] / 2, current_format[1] / 2)

    shaker(thisNode, scale, frequency, scale=thisNode.scale.get())
    shaker(thisNode, translate, frequency, translate=thisNode.translate.get())
    shaker(thisNode, rotate, frequency, rotate=thisNode.rotate.get())


def shaker(thisNode, param, frequency, scale=None, translate=None, rotate=None, restore=True, seed=None):

    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    durations = get_durations(thisNode)

    frequency = 100.0 / frequency
    frequency = value_by_durations(frequency, durations)[thisNode.speed.get()]

    last_frame = duration
    start_frame = 1

    frames = []
    frame_allow = 0

    start = int(start_frame - frequency)
    for frame in range(start, last_frame):
        frames.append(int(frame_allow))

        if frame_allow > last_frame:
            break

        frame_allow += frequency

    # guarda los valores anteriores del key
    prev_dimension_0_values = {}
    prev_dimension_1_values = {}

    for frame in frames:
        prev_dimension_0_values[frame] = param.getValueAtTime(frame, 0)
        prev_dimension_1_values[frame] = param.getValueAtTime(frame, 1)

    if restore:
        for dimension in range(param.getNumDimensions()):
            param.restoreDefaultValue(dimension)

    for frame in frames:
        if scale:
            if seed:
                random.seed(seed + frame + 1)
            scale_value = random.random() * scale - (scale / 2)
            scale_value *= rscale
            if not restore:
                prev_value = prev_dimension_0_values[frame]
                scale_value += prev_value
            else:
                scale_value += 1

            param.setValueAtTime(scale_value, frame, 0)
            param.setValueAtTime(scale_value, frame, 1)

        if translate:
            if seed:
                random.seed(seed + frame + 2)
            x_value = random.random() * translate - (translate / 2)
            x_value *= rscale
            if not restore:
                prev_x_value = prev_dimension_0_values[frame]
                x_value += prev_x_value
            param.setValueAtTime(x_value, frame, 0)

            prev_y_value = prev_dimension_1_values[frame]
            y_value = random.random() * translate - (translate / 2)
            y_value *= rscale
            y_value += prev_y_value
            param.setValueAtTime(y_value, frame, 1)

        if rotate:
            if seed:
                random.seed(seed + frame + 3)
            rotate_value = random.random() * rotate - (rotate / 2)
            if not restore:
                prev_value = prev_dimension_0_values[frame]
                rotate_value += prev_value
            param.setValueAtTime(rotate_value, frame, 0)
