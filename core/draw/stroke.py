from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, get_start_frame, get_transition_duration, reformat_update
from nx import getNode, createNode, get_output, node_delete, get_bbox
from math import sin, radians
import NatronEngine


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def clean_nodes(thisNode):
    count = thisNode.bounces.get()

    for i in range(count, 10):
        transform = getNode(thisNode, 'transform_' + str(i))
        merge = getNode(thisNode, 'merge_' + str(i))
        rectangle = getNode(thisNode, 'rectangle_' + str(i))

        node_delete([rectangle, transform, merge])


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    duration_base = get_duration(thisNode, base=True)
    width, height = get_format(thisNode)
    start_frame = get_start_frame(thisNode)
    last_frame = start_frame + duration
    #

    transition_duration = get_transition_duration(thisNode)

    # Rectangles
    clean_nodes(thisNode)

    size = thisNode.stroke_size.get() * rscale

    bounces = thisNode.bounces.get()

    # 6.45 es el angulo que necesita para 5 trazos, con esto
    # podemos calcular el angulo con la cantidad de trazos.
    rotation = 5 * 6.45 / bounces
    rotation /= 1 + (size * 0.8 / 500)
    height_translate = 0
    height_separation = sin(radians(rotation)) * width
    #

    horizontal = NatronEngine.Natron.KeyframeTypeEnum.eKeyframeTypeHorizontal

    part_duration = transition_duration / bounces
    part_start_frame = start_frame
    last_to_connect = None
    position = 0
    node_position = 0
    for index in range(bounces):

        part_last_frame = part_start_frame + part_duration

        rectangle = createNode('rectangle', 'rectangle_' + str(index), thisNode, force=False)
        rectangle.setPosition(node_position, 0)
        rectangle_size = rectangle.getParam('size')
        rectangle_size.setValue(size, 1)
        rectangle_size.restoreDefaultValue(0)
        rectangle_size.setValueAtTime(0, part_start_frame)
        rectangle_size.setValueAtTime(width, part_last_frame)
        if index == 0:  # Primer rectangulo
            rectangle_size.setInterpolationAtTime(part_start_frame,  horizontal)
        if index == bounces - 1:  # Ultimo rectangulo
            rectangle_size.setInterpolationAtTime(part_last_frame,  horizontal)

        rectangle.getParam('cornerRadius').set(size / 2, size / 2)

        part_start_frame += part_duration
        #

        #

        # Transform
        transform = createNode('transform', 'transform_' + str(index), thisNode, force=False)
        transform.setPosition(node_position, 200)
        transform.connectInput(0, rectangle)
        transform_translate = transform.getParam('translate')
        transform_center = transform.getParam('center')
        transform_rotate = transform.getParam('rotate')

        transform_center.set(size / 2, size / 2)

        if position == 0:
            transform_translate.set(0, height_translate)
            transform_rotate.set(rotation)
            position = 1
        else:
            transform_translate.set(width - size, height_translate)
            transform_rotate.set(180 - rotation)
            position = 0
        #

        #

        # Merge
        if index == 0:
            last_to_connect = transform
        else:
            merge = createNode('merge', 'merge_' + str(index), thisNode, force=False)
            merge.setPosition(node_position, 400)
            merge.connectInput(0, last_to_connect)
            merge.connectInput(1, transform)

            last_to_connect = merge

        #

        height_translate += height_separation
        node_position += 200
    #

    #

    # Correccion Vertical
    bbox = get_bbox(last_to_connect, last_frame)
    y_correction = (height - bbox.y2) / 2

    position = getNode(thisNode, 'position')
    position.getParam('translate').set(0, y_correction)
    position.disconnectInput(0)
    position.connectInput(0, last_to_connect)
    #

    # Reformat
    getNode(thisNode, 'crop').getParam('size').set(width, height)
    #

    #

    # Tiempo
    frame_range = getNode(thisNode, 'frame_range').getParam('frameRange')
    frame_range.set(1, duration_base)

    time_switch = getNode(thisNode, 'time_switch').getParam('which')
    time_switch.restoreDefaultValue()
    mid_duration = duration_base / 2
    time_switch.setValueAtTime(0, mid_duration)
    time_switch.setValueAtTime(1, mid_duration + 1)
    #

    # Inicio del trazo
    start_stroke = thisNode.start_stroke.get()
    mirror = getNode(thisNode, 'mirror')
    flip = mirror.getParam('flip')
    flop = mirror.getParam('flop')

    if start_stroke == 0:
        flip.set(True)
        flop.set(False)

    elif start_stroke == 1:
        flip.set(True)
        flop.set(True)

    elif start_stroke == 2:
        flip.set(False)
        flop.set(False)

    elif start_stroke == 3:
        flip.set(False)
        flop.set(True)
