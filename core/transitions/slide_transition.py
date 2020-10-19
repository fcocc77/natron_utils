from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, limit_transition
from nx import getNode
from animations import exaggerated_animation


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
    width, height = get_format(thisNode)
    start_frame = thisNode.start_frame.get()
    last_frame = start_frame + duration

    direction = thisNode.direction.get()
    gap = thisNode.gap.get() * duration / 100

    translate_a = getNode(thisNode, 'position_a').getParam('translate')
    translate_b = getNode(thisNode, 'position_b').getParam('translate')

    exaggeration = [0.7, 0.7]

    if direction == 0:  # Left
        values_a = [0, -width]
        values_b = [width, 0]
        dimension = 0

    elif direction == 1:  # Right
        values_a = [0, width]
        values_b = [-width, 0]
        dimension = 0

    elif direction == 2:  # Up
        values_a = [0, -height]
        values_b = [height, 0]
        dimension = 1

    elif direction == 3:  # Down
        values_a = [0, height]
        values_b = [-height, 0]
        dimension = 1

    #

    exaggerated_animation(translate_a, duration + gap, start_frame, values_a, exaggeration=exaggeration, dimension=dimension)
    exaggerated_animation(translate_b, duration, start_frame, values_b, exaggeration=exaggeration, dimension=dimension)

    limit_transition(thisNode, start_frame)
