from base import link_to_parent, get_rscale, get_duration, get_format, get_start_frame, get_durations
from nx import getNode
from animations import simple_animation
from vina import value_by_durations


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    duration = get_duration(thisNode)
    durations = get_durations(thisNode)
    width, height = get_format(thisNode)
    start_frame = get_start_frame(thisNode)
    #

    twist_type = thisNode.twist_type.get()

    switch = getNode(thisNode, 'switch').getParam('which')
    switch.set(twist_type)

    if twist_type == 0:
        twist_lines(thisNode, width, height)
    else:
        twist_transition(thisNode, rscale, duration, durations, width, height, start_frame)

    # Crop
    for crop_name in ['crop_a', 'crop_b']:
        crop = getNode(thisNode, crop_name)
        crop_size = crop.getParam('size')
        crop_bottom_left = crop.getParam('bottomLeft')

        crop_size.set(width, width)
        crop_bottom = (width - height) / 2
        crop_bottom_left.set(0, -crop_bottom)
    #

    # End Crop
    end_crop = getNode(thisNode, 'end_crop')
    end_crop.getParam('size').set(width, height)
    end_crop.getParam('bottomLeft').set(0, 0)
    #


def twist_lines(thisNode, width, height):

    # Lines Crop
    crop = getNode(thisNode, 'lines_crop')
    crop_size = crop.getParam('size')
    crop_bottom_left = crop.getParam('bottomLeft')

    crop_height = height * thisNode.lines_area.get() / 100
    crop_bottom = (height / 2) - (crop_height / 2)

    crop_bottom_left.set(0, crop_bottom)
    crop_size.set(width, crop_height)
    #

    # Refresh Lines
    getNode(thisNode, 'lines').getParam('refresh').trigger()
    #


    # Noisier
    noisier = getNode(thisNode, 'noisier')
    evolution = noisier.getParam('evolution')

    evolution.set(thisNode.velocity.get() / 100)


    noisier.getParam('refresh').trigger()
    #

    # Refresh
    getNode(thisNode, 'spin').getParam('refresh').trigger()


def twist_transition(thisNode, rscale, duration, durations, width, height, start_frame):

    # Radial
    radial = getNode(thisNode, 'radial')
    radial_size = radial.getParam('size')
    radial_bottom_left = radial.getParam('bottomLeft')

    radial_height = width
    radial_bottom = (height / 2) - (radial_height / 2)

    radial_size.set(radial_height, radial_height)
    radial_bottom_left.set(0, radial_bottom)
    #

    # Transform
    transform = getNode(thisNode, 'transform')
    scale = transform.getParam('scale')

    scale_y = 0.7
    scale_x = scale_y * thisNode.long.get()
    interpolation = [True, False]

    simple_animation(scale, duration, start_frame, [0, scale_x], interpolation, dimension=0)
    simple_animation(scale, duration, start_frame, [0, scale_y], interpolation, dimension=1)
    #

    # Edge Time
    edge_separation = thisNode.edge_separation.get()
    edges_switch = getNode(thisNode, 'edges').getParam('which')
    if edge_separation:
        edges_switch.set(1)

        edge_separation = value_by_durations(edge_separation, durations)[thisNode.speed.get()]

        edge_inside = getNode(thisNode, 'edge_inside')
        edge_outside = getNode(thisNode, 'edge_outside')

        edge_inside.getParam('timeOffset').set(edge_separation)
        edge_outside.getParam('timeOffset').set(-edge_separation)
    else:
        edges_switch.set(0)
