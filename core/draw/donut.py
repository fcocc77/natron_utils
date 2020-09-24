from base import link_to_parent, get_rscale, get_duration, get_format, get_start_frame
from nx import getNode, createNode, node_delete
from animations import linear_animation, back_and_forth_animation


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def clean_nodes(thisNode):
    transform_amount = thisNode.donut_amount.get()

    for i in range(transform_amount, 20):
        transform = getNode(thisNode, 't' + str(i))
        merge = getNode(thisNode, 'merge' + str(i))

        node_delete([transform, merge])


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    width, height = get_format(thisNode)
    start_frame = get_start_frame(thisNode)
    #

    # Donut
    outside_radial = getNode(thisNode, 'outside_radial')
    inside_radial = getNode(thisNode, 'inside_radial')

    inside_size = inside_radial.getParam('size')
    inside_bottom_left = inside_radial.getParam('bottomLeft')

    outside_size = outside_radial.getParam('size')
    outside_bottom_left = outside_radial.getParam('bottomLeft')

    donut_size = width
    donut_width = thisNode.width.get() * rscale

    inside_size_value = donut_size - donut_width
    inside_bottom_left_value = donut_width / 2

    # Inside Size y BottomLeft Animacion
    input_transition = thisNode.input_transition.get()
    output_transition = thisNode.output_transition.get()

    transition_duration = thisNode.transition_duration.get()
    back_and_forth_animation(inside_size, duration, start_frame,
                             [donut_size + 4, inside_size_value],
                             input=input_transition,
                             output=output_transition,
                             transition=transition_duration)

    back_and_forth_animation(inside_bottom_left, duration, start_frame,
                             [-2, inside_bottom_left_value],
                             input=input_transition,
                             output=output_transition,
                             transition=transition_duration)
    #

    outside_size.set(donut_size, donut_size)
    outside_bottom_left.set(0, 0)
    #

    # Softness
    inside_radial.getParam('softness').set(thisNode.inside_softness.get())
    outside_radial.getParam('softness').set(thisNode.outside_softness.get())
    #

    #
    clean_nodes(thisNode)
    #

    # Transform
    radial_merge = getNode(thisNode, 'radial')
    transform_amount = thisNode.donut_amount.get()
    if not transform_amount:
        return

    separation = (100 - thisNode.time_separation.get()) * duration / 100

    t_duration = duration / transform_amount
    t_start_frame = start_frame
    t_node_pos = 0
    last_transform = None
    last_merge = None
    for i in range(transform_amount):
        t_node_pos += 200

        t = createNode('transform', 't' + str(i), thisNode, position=[t_node_pos, 0], force=False)
        t.connectInput(0, radial_merge)

        if last_transform:
            merge = createNode('merge', 'merge' + str(i), thisNode, position=[t_node_pos, 100], force=False)

            merge.connectInput(1, t)
            if last_merge:
                merge.connectInput(0, last_merge)
            else:
                merge.connectInput(0, last_transform)

            last_merge = merge

        t_center = donut_size / 2
        t.getParam('center').set(t_center, t_center)

        tx = (width / 2) - (donut_size / 2)
        ty = (height / 2) - (donut_size / 2)
        t.getParam('translate').set(tx, ty)

        t_scale_param = t.getParam('scale')

        linear_animation(t_scale_param, t_duration + separation, t_start_frame, [0, 3])

        t_start_frame += t_duration

        last_transform = t

    # Crop
    crop = getNode(thisNode, 'crop')
    crop.disconnectInput(0)
    crop.connectInput(0, last_merge)

    crop.getParam('size').set(width, height)
