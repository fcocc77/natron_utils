# funciones en comun que comparten todas las slides
from nx import getNode, createNode, warning
from base import children_refresh, get_duration, clean


def setup(thisParam, thisNode):
    children_refresh(thisParam, thisNode)
    knob_name = thisParam.getScriptName()

    if knob_name == 'generate_inputs':
        generate_inputs(thisNode)

    if knob_name == 'render':
        twelve_render(thisNode)

    if knob_name == 'refresh':
        set_frame_range(thisNode)

    if knob_name == 'clean':
        clean(thisNode)


def twelve_render(thisNode):
    render = getNode(thisNode, 'TwelveRender')
    render.getParam('render').trigger()


def generate_inputs(thisNode):
    amount = thisNode.input_amount.getValue()
    count = thisNode.getMaxInputCount()

    if amount + 1 <= count:
        warning('Slide inputs', 'Ya existen ' + str(amount) + ' inputs extra.')
        return

    pos = getNode(thisNode, 'Image').getPosition()
    posx = pos[0] + 200
    pasy = pos[1]
    for i in range(amount):
        name = 'E-' + str(i + 1)
        _input = getNode(thisNode, name)
        if not _input:
            _input = createNode('input', name, thisNode, position=[posx, pasy])

        posx += 200


def set_frame_range(slide_node):
    frame_range_node = getNode(slide_node, 'FrameRange')
    if not frame_range_node:
        return

    offset = getNode(slide_node, 'TimeOffset').getParam('timeOffset')
    frame_range = frame_range_node.getParam('frameRange')

    start_frame = slide_node.start_frame.get()
    duration = get_duration(slide_node)

    frame_range.set(start_frame, start_frame + duration)
    offset.set(start_frame)
