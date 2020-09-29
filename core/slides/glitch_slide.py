from base import get_rscale, get_duration, get_format, get_start_frame, get_durations
from animations import simple_animation
from nx import getNode

from slide_common import setup


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    setup(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    durations = get_durations(thisNode)

    current_format = get_format(thisNode)
    start_frame = get_start_frame(thisNode)
    last_frame = start_frame + duration

    #

    # Lines
    lines_noisier = getNode(thisNode, 'lines_noisier')
    lines_noisier_durations = lines_noisier.getParam('durations')

    lines_twist = getNode(thisNode, 'lines_twist')
    lines_twist_durations = lines_twist.getParam('durations')

    lines_offset = getNode(thisNode, 'lines_offset')
    time_offset = lines_offset.getParam('timeOffset')

    # cambiar duracion a los efectos
    speed = thisNode.speed.get()
    lines_duration = durations[speed] / 2

    time_offset.set(last_frame - lines_duration)

    lines_noisier_durations.setValue(lines_duration, speed)
    lines_twist_durations.setValue(lines_duration, speed)
