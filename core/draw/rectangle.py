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

    rectangle = getNode(thisNode, 'rectangle')
    softness_param = rectangle.getParam('softness')
    radius_param = rectangle.getParam('cornerRadius')
    size_param = rectangle.getParam('size')
    bottom_left_param = rectangle.getParam('bottomLeft')

    softness = thisNode.softness.get() * rscale
    softness_param.set(softness)

    radius = thisNode.corner_radius.get() * rscale
    radius_param.set(radius, radius)

    width_percent = thisNode.width.get()
    height_percent = thisNode.height.get()

    new_width = width * width_percent / 100
    new_height = height * height_percent / 100

    size_param.set(new_width, new_height)
    #
    #

    # Bottom Left
    left = 0
    width_align = thisNode.width_align.get()
    if width_align == 0:
        left = (width - new_width) / 2
    elif width_align == 2:
        left = width - new_width

    bottom = 0
    height_align = thisNode.height_align.get()
    if height_align == 0:
        bottom = (height - new_height) / 2
    elif height_align == 1:
        bottom = height - new_height

    bottom_left_param.set(left, bottom)
    #
    #

    # Invert Rectangle
    color_0 = rectangle.getParam('color0')
    color_1 = rectangle.getParam('color1')

    color_param = thisNode.getParam('color_rectangle')

    if color_param:
        color = color_param.get()
        if thisNode.invert.get():
            color_0.set(color[0], color[1], color[2], 1)
            color_1.set(0, 0, 0, 0)
        else:
            color_1.set(color[0], color[1], color[2], 1)
            color_0.set(0, 0, 0, 0)

    else:

        if thisNode.invert.get():
            color_0.set(1, 1, 1, 1)
            color_1.set(0, 0, 0, 0)
        else:
            color_1.set(1, 1, 1, 1)
            color_0.set(0, 0, 0, 0)
