from base import link_to_parent, children_refresh, get_rscale, get_duration, get_format, get_start_frame
from nx import getNode
from text_fit import refresh_text_fit
from text_base import transfer_transform


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
    duration = get_duration(thisNode)
    width, height = get_format(thisNode)
    start_frame = get_start_frame(thisNode)
    last_frame = start_frame + duration

    refresh_text_fit(thisNode)

    # Stroke Transform
    parent_transform = thisNode.getInput(0)
    stroke_transform = getNode(thisNode, 'stroke_transform')
    transfer_transform(parent_transform, stroke_transform)
    #

    # Color de trazo
    grade = getNode(thisNode, 'grade')
    white = grade.getParam('white')
    for dimension in range(3):
        color = thisNode.subtitle_color.getValue(dimension)
        white.setValue(color, dimension)
