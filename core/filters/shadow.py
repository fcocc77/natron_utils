from base import link_to_parent, children_refresh, get_rscale, get_format
from nx import getNode, get_bbox
from math import cos, sin


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    current_format = get_format(thisNode)

    distance = thisNode.shadow_distance.get() * rscale
    opacity = thisNode.shadow_opacity.get()
    blur = thisNode.shadow_blur.get() * rscale
    angle = thisNode.shadow_angle.get()

    inside = thisNode.shadow_inside.get()

    getNode(thisNode, 'blur').getParam('size').set(blur, blur)

    getNode(thisNode, 'merge').getParam('mix').set(opacity)
    getNode(thisNode, 'inside_merge').getParam('mix').set(opacity)

    inside_switch = getNode(thisNode, 'inside_switch').getParam('which')
    inside_switch.set(inside)

    angle /= 57.0

    X = distance * cos(angle)
    Y = distance * sin(angle)
    translate = getNode(thisNode, 'position').getParam('translate')
    translate.set(X, Y)

    if inside:
        crop = getNode(thisNode, 'crop')
        bbox = get_bbox(thisNode.getInput(0))

        size = crop.getParam('size')
        bottom_left = crop.getParam('bottomLeft')

        size.set(bbox.x2 - bbox.x1, bbox.y2 - bbox.y1)
        bottom_left.set(bbox.x1, bbox.y1)
