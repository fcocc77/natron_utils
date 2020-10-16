from base import link_to_parent, children_refresh, get_rscale, get_format, get_duration, get_start_frame
from nx import getNode


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)

    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    duration = get_duration(thisNode)
    start_frame = get_start_frame(thisNode)
    last_frame = start_frame + duration
