from base import link_to_parent, children_refresh, get_format, get_rscale
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

    radial = getNode(thisNode, 'Radial')
    size = radial.getParam('size')
    bottom_left = radial.getParam('bottomLeft')

    radial_added = width * thisNode.radial_expand.get()

    size_x = width + radial_added
    size_y = height + radial_added
    size.set(size_x, size_y)
    bl = -radial_added / 2
    bottom_left.set(bl, bl)

    # Blur
    blur = getNode(thisNode, 'blur')
    blur_size = thisNode.blur.get() * rscale
    blur.getParam('size').set(blur_size, blur_size)
    #
    #
