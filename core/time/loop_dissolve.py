from base import link_to_parent, children_refresh, get_rscale, get_format
from nx import getNode, warning, createNode, node_delete
from animations import simple_animation
from math import ceil


def main(thisParam, thisNode, thisGroup, app, userEdited):
    if not userEdited:
        return

    knob_name = thisParam.getScriptName()

    if knob_name == 'refresh':
        refresh(thisNode)

    link_to_parent(thisNode, thisParam, thisGroup)
    children_refresh(thisParam, thisNode)


def loop(thisNode, offset_a_name, offset_b_name, dissolve_name, frame_range_name, frames):

    dissolve = getNode(thisNode, dissolve_name).getParam('which')
    offset_a = getNode(thisNode, offset_a_name).getParam('timeOffset')
    offset_b = getNode(thisNode, offset_b_name).getParam('timeOffset')
    frame_range_node = getNode(thisNode, frame_range_name)

    mid_frame = frames / 2

    duration = thisNode.transition_duration.get()
    start_frame = mid_frame - duration

    simple_animation(dissolve, duration, start_frame, [0, 1])

    offset_a.set(-mid_frame)
    offset_b.set(mid_frame - duration)

    # Frame Range Final
    correct_last_frame = frames - duration

    frame_range = frame_range_node.getParam('frameRange')
    frame_range.set(1, correct_last_frame)
    #
    #

    return frame_range_node


def refresh(thisNode):
    rscale = get_rscale(thisNode)
    width, height = get_format(thisNode)

    input_node = thisNode.getInput(0)
    output_switch = getNode(thisNode, 'output_switch')

    # Warning
    ok = True
    if not input_node:
        ok = False
    elif input_node.getPluginID() != 'fr.inria.built-in.Read':
        ok = False

    if not ok:
        warning('Error de Coneccion', '!Debe Conectar un nodo "Read"')
        return
    #
    #

    # Loop
    input_frames = input_node.getParam('lastFrame').get()
    transition_duration = thisNode.transition_duration.get()
    output_frames = thisNode.frames.get()

    total_frames = output_frames + transition_duration

    output_dot = getNode(thisNode, 'output_dot')
    output_dot.disconnectInput(0)
    if input_frames >= total_frames:
        read_node_input = getNode(thisNode, 'ReadNode')
        output_dot.connectInput(0, read_node_input)
    else:
        output_dot.connectInput(0, output_switch)

    loop(thisNode, 'offset_a2', 'offset_b2', 'dissolve2', 'final_range', total_frames)
    last_node_to_connect = loop(thisNode, 'offset_a', 'offset_b', 'dissolve', 'frame_range', input_frames)
    #
    #

    # Repeticion de Time Offset
    correct_last_frame = input_frames - transition_duration
    number_of_repetitions = int(ceil(float(output_frames) / float(correct_last_frame))) + 1

    output_switch_which = output_switch.getParam('which')
    output_switch_which.restoreDefaultValue()

    # borra nodos sobrante
    for i in range(number_of_repetitions, 30):
        node_to_delete = getNode(thisNode, 'offset_' + str(i))
        if node_to_delete:
            output_switch.disconnectInput(i)
            node_delete(node_to_delete)

    #

    node_position_x = 0
    offset = 0
    for repeat in range(number_of_repetitions):
        offset_node = createNode('time_offset', 'offset_' + str(repeat), thisNode, force=False)
        offset_node.connectInput(0, last_node_to_connect)
        offset_node.setPosition(node_position_x, 100)

        offset_node.getParam('timeOffset').set(offset)

        output_switch.connectInput(repeat, offset_node)
        output_switch_which.setValueAtTime(repeat, offset + 1)

        offset += correct_last_frame
        node_position_x += 200
