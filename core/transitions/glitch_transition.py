from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, get_start_frame
from nx import getNode
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
    current_format = get_format(thisNode)
    start_frame = get_start_frame(thisNode)

    ray_blur_param = getNode(thisNode, 'ray_blur').getParam('size')

    lens_distort = getNode(thisNode, 'lens_distort')
    k1_param = lens_distort.getParam('k1')
    center_param = lens_distort.getParam('center')

    # restaurar valores
    ray_blur_param.restoreDefaultValue(0)
    ray_blur_param.restoreDefaultValue(1)

    ray_blur_amount = 400

    direction = thisNode.direction.get()
    if direction <= 1:  # horizontal
        vertical = False
        blur_dimension = 0

        if direction == 0:  # Left
            center = [-1, 0]

        elif direction == 1:  # Right
            center = [1, 0]

    else:  # Vertical
        vertical = True
        blur_dimension = 1

        if direction == 2:  # Up
            center = [0, -1]

        elif direction == 3:  # Down
            center = [0, 1]

    center_param.set(center[0], center[1])

    back_and_forth_animation(k1_param, duration, start_frame, [0, 0.2])

    back_and_forth_animation(ray_blur_param, duration, start_frame,  [0, ray_blur_amount], dimension=blur_dimension)

    adjust_edge_mask(thisNode, start_frame, duration)
    chromatic_aberration(thisNode, start_frame, duration, vertical, rscale)

    # erode
    erode = getNode(thisNode, 'erode').getParam('size')
    erode.restoreDefaultValue(0)
    erode.restoreDefaultValue(1)

    if vertical:
        erode_dimension = [1, 0]
    else:
        erode_dimension = [0, 1]

    back_and_forth_animation(erode, duration, start_frame,  [0, -50], dimension=erode_dimension[0])
    back_and_forth_animation(erode, duration, start_frame,  [0, -20], dimension=erode_dimension[1])


def chromatic_aberration(thisNode, start_frame, duration, vertical, rscale):

    green_translate = getNode(thisNode, 'green_position').getParam('translate')
    blue_translate = getNode(thisNode, 'blue_position').getParam('translate')

    separation = 10 * rscale

    if vertical:
        dimension = 1
    else:
        dimension = 0

    back_and_forth_animation(green_translate, duration, start_frame,  [0, separation], dimension=dimension)
    back_and_forth_animation(blue_translate, duration, start_frame,  [0, -separation], dimension=dimension)


def adjust_edge_mask(thisNode,  start_frame, duration):

    last_frame = start_frame + duration

    duration_part = duration / 4

    # edge mask
    edge_mask = getNode(thisNode, 'edge_mask').getParam('toleranceLower')

    edge_mask.restoreDefaultValue()

    edge_mask.setValueAtTime(-1, start_frame)
    edge_mask.setValueAtTime(0, start_frame + duration_part)

    edge_mask.setValueAtTime(0, last_frame - duration_part)
    edge_mask.setValueAtTime(-1, last_frame)
