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
    width, height = get_format(thisNode)

    constant = getNode(thisNode, 'constant')
    constant.getParam('size').set(width, height)
