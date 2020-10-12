from base import link_to_parent, children_refresh, get_rscale, get_format
from nx import getNode


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
    width, height = get_format(thisNode)

    # Transforms
    transform_left = getNode(thisNode, 'transform_left')
    transform_right = getNode(thisNode, 'transform_right')
    transform_top = getNode(thisNode, 'transform_top')
    transform_bottom = getNode(thisNode, 'transform_bottom')

    transform_left.getParam('scale').set(-1, 1)
    transform_right.getParam('scale').set(-1, 1)
    transform_top.getParam('scale').set(1, -1)
    transform_bottom.getParam('scale').set(1, -1)

    center = [width / 2, height / 2]
    transform_left.getParam('center').set(*center)
    transform_right.getParam('center').set(*center)
    transform_top.getParam('center').set(*center)
    transform_bottom.getParam('center').set(*center)

    transform_left.getParam('translate').set(-width, 0)
    transform_right.getParam('translate').set(width, 0)
    transform_top.getParam('translate').set(0, -height)
    transform_bottom.getParam('translate').set(0, height)
    #
    #

    # Global Transform
    tranform_global = getNode(thisNode, 'tranform_global')
    tranform_global.getParam('center').set(*center)

    scale_percent = thisNode.scale.get()
    scale_size = 1 - ((1 - (1.0 / 3)) * scale_percent / 100)

    tranform_global.getParam('scale').set(scale_size, scale_size)
