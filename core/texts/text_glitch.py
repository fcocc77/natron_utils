from base import link_to_parent, children_refresh, get_rscale, get_duration, get_start_frame, reformat_update
from nx import getNode, get_bbox
from text_fit import refresh_text_fit
from animations import back_and_forth_animation


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
    start_frame = get_start_frame(thisNode)
    transition_duration = thisNode.transition_duration.get()

    orientation = thisNode.orientation.get()

    refresh_text_fit(thisNode)
    reformat_update(thisNode, getNode(thisNode, 'reformat'))

    # Checker
    checker = getNode(thisNode, 'checker')
    box_size = thisNode.box_size.get() * rscale

    bbox = get_bbox(getNode(thisNode, 'titles_merge'))

    bottom = bbox.x1 - box_size
    left = bbox.y1 - box_size
    size_x = bbox.x2 - bottom + box_size
    size_y = bbox.y2 - left + box_size

    checker.getParam('bottomLeft').set(bottom, left)
    checker.getParam('size').set(size_x, size_y)
    checker.getParam('boxSize').set(box_size, box_size)
    #

    #

    # Gap
    gap_translate = getNode(thisNode, 'gap').getParam('translate')
    gap_translate.set(-box_size, 0)
    #

    #

    # Checker Position
    checker_translate = getNode(thisNode, 'checker_position').getParam('translate')
    checker_translate.restoreDefaultValue(0)
    checker_translate.restoreDefaultValue(1)

    back_and_forth_animation(checker_translate, duration, start_frame, [0, box_size], transition_duration, dimension=orientation)
    #

    #

    # Desplazamiento de las 2 partes
    part_a = getNode(thisNode, 'part_a').getParam('translate')
    part_b = getNode(thisNode, 'part_b').getParam('translate')

    part_a.restoreDefaultValue(0)
    part_a.restoreDefaultValue(1)
    part_b.restoreDefaultValue(0)
    part_b.restoreDefaultValue(1)

    separation = thisNode.separation.get() * rscale

    back_and_forth_animation(part_b, duration, start_frame, [separation, 0], transition_duration, dimension=orientation)
    back_and_forth_animation(part_a, duration, start_frame, [-separation, 0], transition_duration, dimension=orientation)
    #

    #

    # Glitch
    orientation_glitch = getNode(thisNode, 'orientation_glitch').getParam('which')
    orientation_glitch.set(orientation)

    distort_param = getNode(thisNode, 'distort').getParam('uvScale')

    distort = thisNode.distort.get() * rscale
    distort_param.set(distort, distort)

    distort_switch = getNode(thisNode, 'distort_switch').getParam('which')

    if distort:
        distort_switch.set(1)
    else:
        distort_switch.set(0)
    #
