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
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    durations = get_durations(thisNode)
    current_format = get_format(thisNode)

    transform = getNode(thisNode, 'transform')

    translate = transform.getParam('translate')
    center = transform.getParam('center')
    scale = transform.getParam('scale')
    rotate = transform.getParam('rotate')

    scale.restoreDefaultValue(0)
    scale.restoreDefaultValue(1)
    translate.restoreDefaultValue(0)
    translate.restoreDefaultValue(1)
    rotate.restoreDefaultValue(0)

    frequency = 100.0 / thisNode.frequency.get()
    frequency = value_by_durations(frequency, durations)[thisNode.speed.get()]

    last_frame = duration
    start_frame = 1

    frames = []
    frame_allow = 0

    center.set(current_format[0] / 2, current_format[1] / 2)

    start = int(start_frame - frequency)
    for frame in range(start, last_frame):
        frames.append(int(frame_allow))
        if frame_allow > last_frame:
            break

        frame_allow += frequency

    for frame in frames:

        if thisNode.scale.get():
            scale_value = random.random() * thisNode.scale.get()
            scale_value *= rscale
            scale_value += 1

            scale.setValueAtTime(scale_value, frame, 0)
            scale.setValueAtTime(scale_value, frame, 1)

        if thisNode.translate.get():
            x_value = random.random() * thisNode.translate.get() - (thisNode.translate.get() / 2)
            x_value *= rscale
            translate.setValueAtTime(x_value, frame, 0)

            y_value = random.random() * thisNode.translate.get() - (thisNode.translate.get() / 2)
            y_value *= rscale
            translate.setValueAtTime(y_value, frame, 1)

        if thisNode.rotate.get():
            rotate_value = random.random() * thisNode.rotate.get() - (thisNode.rotate.get() / 2)
            rotate.setValueAtTime(rotate_value, frame, 0)
