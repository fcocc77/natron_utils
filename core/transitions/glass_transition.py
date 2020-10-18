import os
import NatronEngine
from nx import getNode, alert, switch, get_connected_nodes, question, node_delete, warning, input_connected, dots_delete
from base import link_to_parent, children_refresh, get_rscale, get_format, limit_transition, clean
from vina import value_by_durations
from general import formats


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)
    if knob_name == 'clean':
        clean(thisNode)
    if knob_name == 'render':
        getNode(thisNode, 'TwelveRender').getParam('render').trigger()

    children_refresh(thisParam, thisNode)


def refresh(thisNode):

    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    start_frame = thisNode.start_frame.get()

    start_frame_node = getNode(thisNode, 'start_frame_node')
    start_frame_node.getParam('timeOffset').set(start_frame)

    # Glass Blur
    glass_blur = getNode(thisNode, 'glass_blur').getParam('size')
    blur_size = 4 * rscale
    glass_blur.set(blur_size, blur_size)
    #
    #

    # Transform
    glass_transform = getNode(thisNode, 'glass_transform')
    glass_transform.getParam('center').set(width / 2, height / 2)
    #
    #

    limit_transition(thisNode, start_frame)
