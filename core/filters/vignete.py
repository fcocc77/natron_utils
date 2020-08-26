from base import link_to_parent, children_refresh
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
    radial = getNode(thisNode, 'Radial')
    size = radial.getParam('size')

    current_format = thisNode.getParam('current_format').get()

    size.set(current_format[0], current_format[1])
