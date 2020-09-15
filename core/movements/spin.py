from base import link_to_parent, children_refresh, get_duration, get_start_frame
from nx import getNode
from movements_common import center_from_input_bbox


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()
    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)

    if knob_name == 'refresh':
        refresh(thisNode)


def refresh(thisNode):
    duration = get_duration(thisNode)

    first_frame = get_start_frame(thisNode)
    last_frame = first_frame + duration

    transform = getNode(thisNode, 'transform')
    rotate = transform.getParam('rotate')
    center = transform.getParam('center')

    rotate.restoreDefaultValue()

    velocity = thisNode.velocity.get() * 10

    if thisNode.direction.get():
        value = -velocity
    else:
        value = velocity

    rotate.setValueAtTime(0, first_frame)
    rotate.setValueAtTime(value, last_frame)

    center_from_input_bbox(thisNode, center)
