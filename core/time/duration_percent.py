from base import link_to_parent, children_refresh, get_start_frame
from nx import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    start_frame = get_start_frame(thisNode)

    time_offset = getNode(thisNode, 'time_offset').getParam('timeOffset')
    time_offset.set(start_frame)
