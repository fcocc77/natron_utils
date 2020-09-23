from base import link_to_parent, children_refresh, get_rscale, get_format
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

    x2_param = getNode(thisNode, 'x2').getParam('size')
    x4_param = getNode(thisNode, 'x4').getParam('size')
    x8_param = getNode(thisNode, 'x8').getParam('size')

    size = thisNode.size.get() * rscale

    x2 = size * 2
    x4 = size * 4
    x8 = size * 8

    x2_param.set(x2, x2)
    x4_param.set(x4, x4)
    x8_param.set(x8, x8)

    getNode(thisNode, 'mix').getParam('mix').set(thisNode.opacity.get())
    #

    # Grade
    grade = getNode(thisNode, 'grade')
    gamma_param = grade.getParam('gamma')
    color_param = grade.getParam('white')

    for dimension in range(4):
        gamma_param.setValue(thisNode.gamma.get(), dimension)
        color_param.setValue(thisNode.color.getValue(dimension), dimension)
