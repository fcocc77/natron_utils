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

    chromatic_aberration(thisNode, start_frame, duration, rscale)
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


def chromatic_aberration(thisNode, start_frame, duration, rscale, vertical=False):

    last_frame = start_frame + duration

    red_translate = getNode(thisNode, 'red_position').getParam('translate')
    blue_translate = getNode(thisNode, 'blue_position').getParam('translate')

    amount = 10

    separation = amount * rscale

    if vertical:
        dimension = 1
    else:
        dimension = 0

    duration /= 4

    # Entrada
    simple_animation(red_translate, duration, start_frame, [-separation, 0], dimension=dimension)
    simple_animation(blue_translate, duration, start_frame, [separation, 0], dimension=dimension)

    # Salida
    start_frame_output = last_frame - duration
    simple_animation(red_translate, duration, start_frame_output, [0, -separation], restore=False, dimension=dimension)
    simple_animation(blue_translate, duration, start_frame_output, [0, separation], restore=False, dimension=dimension)
