from base import link_to_parent, children_refresh, get_duration, get_start_frame, reformat_update, get_format
from nx import getNode
from animations import exaggerated_animation


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
    start_frame = get_start_frame(thisNode)
    current_format = get_format(thisNode)

    transition_duration = thisNode.transition_duration.get() * duration / 100
    last_frame = start_frame + transition_duration

    getNode(thisNode, 'crop').getParam('size').set(current_format[0], current_format[1])

    # formato de entrada
    reformat_input = getNode(thisNode, 'reformat_input')
    scale = 1 - thisNode.pixel_size.get() / 101.0

    scale_param = reformat_input.getParam('reformatScale')
    exaggerated_animation(scale_param, transition_duration, start_frame, [scale, 0.25])

    reformat = getNode(thisNode, 'reformat')
    reformat_update(thisNode, reformat)

    # cambia al original en el ultimo frame
    switch = getNode(thisNode, 'switch').getParam('which')
    switch.restoreDefaultValue()
    switch.setValueAtTime(0, last_frame)
    switch.setValueAtTime(1, last_frame + 1)
