from base import link_to_parent, get_rscale, get_format
from nx import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    checker = getNode(thisNode, 'pixels')
    box_size = checker.getParam('boxSize')
    line_width = checker.getParam('lineWidth')

    size = int(thisNode.size.get() * rscale)
    box_size.set(size, size)

    space = int(thisNode.space.get() * rscale)
    line_width.set(space)

    checker.getParam('size').set(width, height)
