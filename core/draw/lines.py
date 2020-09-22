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

    # Checker
    checker = getNode(thisNode, 'checker')
    box_size = checker.getParam('boxSize')
    color_0 = checker.getParam('color0')
    color_1 = checker.getParam('color1')
    color_2 = checker.getParam('color2')
    color_3 = checker.getParam('color3')

    checker.getParam('size').set(width, height)

    separation = thisNode.separation.get() * rscale
    box_size.set(separation, separation)

    orientation = thisNode.orientation.get()

    for color in [color_0, color_1, color_2, color_3]:
        color.set(0, 0, 0, 0)

    if orientation == 0:
        color_0.set(1, 1, 1, 1)
        color_1.set(1, 1, 1, 1)
    else:
        color_1.set(1, 1, 1, 1)
        color_2.set(1, 1, 1, 1)
    #

    # Grosor
    translate = getNode(thisNode, 'position').getParam('translate')

    thickness = thisNode.thickness.get() * rscale

    if orientation:
        translate.set(thickness, 0)
    else:
        translate.set(0, thickness)
    #

    getNode(thisNode, 'crop').getParam('size').set(width, height)
